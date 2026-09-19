"""Prove the validator catches security regressions in otherwise valid pages."""
import unittest
from check import Page, ROOT, check_css


class SecurityChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'index.html').read_text()

    def injected(self, markup):
        return self.source.replace('</main>', markup + '</main>')

    def test_current_page_passes(self):
        self.assertEqual(Page(self.source).errors, [])

    def test_rejects_active_content(self):
        for markup in [
            '<script src="https://example.com/a.js"></script>',
            '<iframe src="https://example.com"></iframe>',
            '<a href="javascript:alert(1)">bad</a>',
            '<a href="java\nscript:alert(1)">bad</a>',
            '<img src="/favicon.svg" alt="" width="1" height="1" onerror="alert(1)">',
            '<base href="https://example.com">',
            '<form action="https://example.com"></form>',
            '<div style="color:red">bad</div>',
            '<img src="https://example.com/pixel" alt="" width="1" height="1">',
            '<a href="//example.com">bad</a>',
            '<a href="https://example.com" target="_blank">bad</a>',
        ]:
            with self.subTest(markup=markup):
                self.assertTrue(Page(self.injected(markup)).errors)

    def test_rejects_weakened_policy(self):
        self.assertTrue(Page(self.source.replace("script-src 'none'", "script-src 'self' 'unsafe-inline'")).errors)

    def test_rejects_missing_referrer_policy(self):
        self.assertTrue(Page(self.source.replace('content="no-referrer"', 'content="unsafe-url"')).errors)

    def test_rejects_remote_or_escaped_css_urls(self):
        for css in [
            '@import "https://example.com/style.css";',
            'x { background: url(https://example.com/pixel); }',
            r'x { background: url(\68ttps://example.com/pixel); }',
            r'@im\70ort "https://example.com/style.css";',
            'x { background: url(//example.com/pixel); }',
            'x { background: url(/css/fonts/../../../private.woff); }',
        ]:
            with self.subTest(css=css): self.assertTrue(check_css(css))
        self.assertFalse(check_css("@font-face { src: url('/css/fonts/FiraSans-Light.woff'); }"))

    def test_rejects_malformed_markup(self):
        self.assertTrue(Page(self.injected('<p><div>bad</div></p>')).errors)


if __name__ == '__main__':
    unittest.main()
