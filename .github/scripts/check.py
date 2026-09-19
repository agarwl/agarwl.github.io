#!/usr/bin/env python3
"""Offline security, HTML structure, metadata, and local-link checks. No dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
FORBIDDEN = {'script', 'iframe', 'frame', 'object', 'embed', 'base', 'form', 'style', 'svg', 'math'}
REQUIRED_CSP = {
    'default-src': "'none'", 'script-src': "'none'", 'style-src': "'self'",
    'img-src': "'self'", 'font-src': "'self'", 'connect-src': "'none'",
    'frame-src': "'none'", 'object-src': "'none'", 'base-uri': "'none'",
    'form-action': "'none'", 'upgrade-insecure-requests': '',
}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.errors, self.stack, self.ids, self.links = [], [], set(), []
        self.h1 = self.main = self.csp_count = 0
        self.title = self.description = self.canonical = self.referrer = False
        self.feed(source)
        self.close()
        if self.stack:
            self.errors.append('Unclosed tags: ' + ', '.join(self.stack))
        if self.h1 != 1 or self.main != 1:
            self.errors.append('Require exactly one h1 and one main')
        if not all([self.title, self.description, self.canonical, self.referrer, self.csp_count == 1]):
            self.errors.append('Missing title, description, canonical, referrer policy, or unique CSP')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if len(a) != len(attrs):
            self.errors.append(f'Duplicate attributes on {tag}')
        if tag in FORBIDDEN:
            self.errors.append(f'Forbidden element: {tag}')
        if tag == 'html' and a.get('lang') != 'en':
            self.errors.append('Missing document language')
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'title': self.title = True
        if tag == 'a' and 'a' in self.stack:
            self.errors.append('Nested anchor')
        if tag in {'div', 'p', 'h1', 'h2', 'h3', 'ul', 'section', 'article'} and 'p' in self.stack:
            self.errors.append(f'Invalid {tag} inside paragraph')
        if a.get('id'):
            if a['id'] in self.ids: self.errors.append('Duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if a.get('target') == '_blank' and not {'noopener', 'noreferrer'} <= set(a.get('rel', '').split()):
            self.errors.append('New tab link requires noopener noreferrer')
        for key, value in attrs:
            if key.startswith('on') or key in {'style', 'srcdoc', 'srcset', 'ping'}:
                self.errors.append(f'Forbidden attribute: {key}')
            if key in {'href', 'src', 'action', 'poster', 'data'}:
                value = value or ''
                url = urlsplit(value)
                if url.scheme not in {'', 'https', 'mailto'} or value.startswith('//') or '\\' in value or any(ord(c) < 32 for c in value):
                    self.errors.append('Unsafe URL: ' + value)
                if key != 'href' or tag != 'a':
                    if url.netloc and not (tag == 'link' and a.get('rel') == 'canonical'):
                        self.errors.append('Remote subresource: ' + value)
                self.links.append((tag, key, value))
        if tag == 'img' and not all(x in a for x in ['alt', 'width', 'height']):
            self.errors.append('Image missing alt text or dimensions')
        if tag in {'img', 'link'} and not self.csp_count:
            self.errors.append('Resource appears before CSP')
        if tag == 'meta':
            if a.get('http-equiv', '').lower() == 'content-security-policy':
                self.csp_count += 1
                directives = {}
                for part in a.get('content', '').split(';'):
                    tokens = part.strip().split(None, 1)
                    if tokens:
                        if tokens[0] in directives: self.errors.append('Duplicate CSP directive')
                        directives[tokens[0]] = tokens[1] if len(tokens) > 1 else ''
                if directives != REQUIRED_CSP:
                    self.errors.append('CSP must deny active content and allow only local CSS/images/fonts')
            if a.get('name') == 'referrer': self.referrer = a.get('content') == 'no-referrer'
            if a.get('name') == 'description': self.description = bool(a.get('content'))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href', '').startswith('https://agarwl.github.io/')
        if tag not in VOID: self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID: self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f'Mismatched closing {tag}; expected {self.stack[-1] if self.stack else "none"}')
        else:
            self.stack.pop()


def check_css(source):
    errors = []
    # Decode escapes before auditing so an escaped scheme or @import is caught.
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.S)
    source = re.sub(r'\\([0-9a-fA-F]{1,6})\s?', lambda m: chr(int(m[1], 16)), source)
    source = re.sub(r'\\(.)', r'\1', source)
    if re.search(r'@import|expression\s*\(', source, re.I):
        errors.append('CSS imports and executable expressions are forbidden')
    for value in re.findall(r'url\s*\(\s*([^)]*?)\s*\)', source, re.I):
        value = value.strip('\"\' ')
        url = urlsplit(value)
        target = (ROOT / unquote(url.path).lstrip('/')).resolve()
        if url.scheme or url.netloc or not value.startswith('/css/fonts/') or not target.is_relative_to(ROOT / 'css/fonts'):
            errors.append('Only local font URLs are allowed in CSS: ' + value)
        elif not target.is_file():
            errors.append('Missing font: ' + value)
    return errors


def main():
    files = sorted(p for p in ROOT.rglob('*.html') if not any(x.startswith('.') for x in p.relative_to(ROOT).parts))
    pages = {p: Page(p.read_text()) for p in files}
    errors = []
    for path, page in pages.items():
        errors.extend(f'{path.relative_to(ROOT)}: {e}' for e in page.errors)
        for tag, key, value in page.links:
            url = urlsplit(value)
            if url.scheme or url.netloc: continue  # Project sites share this origin but live in other repositories.
            target = ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
            if not url.path: target = path
            if target.is_dir(): target /= 'index.html'
            if not target.exists() and not target.suffix: target = target.with_suffix('.html')
            target = target.resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f'{path.relative_to(ROOT)}: Missing local resource {value}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: Missing anchor {value}')
    for path in ROOT.glob('css/*.css'):
        errors.extend(f'{path.name}: {error}' for error in check_css(path.read_text()))
    for name in ['atom.xml', 'sitemap.xml', 'favicon.svg']:
        ET.parse(ROOT / name)
    svg = ET.parse(ROOT / 'favicon.svg')
    for el in svg.iter():
        if el.tag.split('}')[-1] not in {'svg', 'rect', 'text'} or any(k.startswith('on') or k.split('}')[-1] == 'href' for k in el.attrib):
            errors.append('Favicon contains active or external content')
    if not (ROOT / '.nojekyll').exists(): errors.append('Missing .nojekyll')
    if list(ROOT.rglob('*.js')): errors.append('JavaScript assets must not be shipped')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'PASS: {len(pages)} pages; strict CSP, HTML structure, local resources, anchors, XML, and no runtime dependencies.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
