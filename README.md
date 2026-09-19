# Rishabh Agarwal’s website

A static academic website for [agarwl.github.io](https://agarwl.github.io/). No JavaScript, third-party runtime assets, package manager, or installed build dependencies are required.

## Edit and preview

Edit page content and the shared layout in `.github/site/`, and styles in `css/main.css`. Use Python 3.9 or newer:

```sh
python3 .github/scripts/build.py
python3 .github/scripts/check.py
python3 -m unittest discover -s .github/scripts -p 'test_*.py'
python3 .github/scripts/serve.py
```

Open <http://127.0.0.1:8765>. The preview binds only to loopback, supports extensionless page URLs, and serves the custom 404. It is a development helper, not a production server.

Commit both source templates and the generated HTML. CI runs `build.py --check` to prevent stale output. The Python renderer uses the standard library; it does not download packages or execute content as code.

## Publishing

GitHub Pages continues serving the repository root on `master`. `.nojekyll` makes the committed HTML directly deployable without Ruby, Jekyll, plugins, or a custom Actions deployment. `/`, `/research`, `/research.html`, `/talks`, `/talks.html`, `/beta/`, the custom 404, and the Atom feed remain available. GitHub Pages handles the extensionless HTML routes. Existing project websites such as `/rliable/` are separate repositories and are not modified here.

Merge only after reviewing the preview and the `Site checks` workflow. Keep **Enforce HTTPS** enabled in Pages settings. See [the security review](.github/SECURITY-REVIEW.md) for checks performed and hosting limitations.

## Licensing

The original site is [MIT licensed](LICENSE).
