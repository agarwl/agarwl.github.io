#!/usr/bin/env python3
"""Render the checked-in static pages using only the Python standard library."""
import argparse
import hashlib
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '.github' / 'site'
PAGES = {
    'index.html': ('Rishabh Agarwal', '/', 'about', 'Reinforcement learning, language models, and AI for scientific discovery. Founding member at Periodic Labs and Adjunct Professor at McGill University.'),
    'research.html': ('Research — Rishabh Agarwal', '/research', 'research', 'Selected research on reinforcement learning, language models, distillation, and reliable evaluation.'),
    'talks.html': ('Talks — Rishabh Agarwal', '/talks', 'talks', 'Talks and tutorials by Rishabh Agarwal on reinforcement learning and language models.'),
    '404.html': ('Page not found — Rishabh Agarwal', '/404.html', '', 'This page could not be found. Explore research and talks by Rishabh Agarwal.'),
    'beta/index.html': ('Rishabh Agarwal', '/', '', 'Continue to Rishabh Agarwal’s homepage.'),
}


def render():
    asset_version = hashlib.sha256(b''.join((ROOT / path).read_bytes() for path in ['css/main.css', 'css/fonts.css'])).hexdigest()[:12]
    template = Template((SOURCE / 'layout.html').read_text())
    for filename, (title, path, active, description) in PAGES.items():
        content = (SOURCE / filename).read_text()
        content = template.substitute(
            title=escape(title), description=escape(description, quote=True), asset_version=asset_version,
            canonical='https://agarwl.github.io' + path, content=content,
            about_current=' aria-current="page"' if active == 'about' else '',
            research_current=' aria-current="page"' if active == 'research' else '',
            talks_current=' aria-current="page"' if active == 'talks' else '',
            extra_meta='<meta http-equiv="refresh" content="0; url=/">' if filename.startswith('beta/') else
                       '<meta name="robots" content="noindex">' if filename == '404.html' else '',
        )
        yield ROOT / filename, '\n'.join(line.rstrip() for line in content.splitlines()) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed pages are stale')
    args = parser.parse_args()
    stale = []
    for path, content in render():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        parser.exit(1, 'Run python3 .github/scripts/build.py; stale pages: ' + ', '.join(stale) + '\n')
    print('Static pages are up to date.' if args.check else 'Rendered 5 static pages.')


if __name__ == '__main__':
    main()
