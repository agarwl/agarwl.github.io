# Rishabh Agarwal’s website

The static site at [agarwl.github.io](https://agarwl.github.io/), with a warm, responsive academic layout inspired by [Periodic Labs](https://periodic.com/). It loads no JavaScript or third-party runtime resources. Typography uses system fonts; styles, images, and icon fonts are hosted locally.

## Edit and preview

Edit page content and the shared layout in `.github/site/`, and styles in `css/`. Use Python 3.9 or newer:

```sh
python3 .github/scripts/build.py
python3 .github/scripts/check.py
python3 -m unittest discover -s .github/scripts -p 'test_*.py'
python3 .github/scripts/serve.py
```

Open <http://127.0.0.1:8765>. The development preview binds only to loopback, supports extensionless URLs, and serves the custom 404.

Commit the source templates and generated HTML together. CI runs `build.py --check` to prevent stale output. The renderer and checks use only the Python standard library; they do not download packages or execute page content as code. Stylesheet URLs include a content digest to prevent stale cached styles after an update.

## Publishing

GitHub Pages continues serving the repository root on `master`. `.nojekyll` publishes the committed HTML without Ruby, Jekyll, plugins, or a custom Actions deployment. `/`, `/research`, `/research.html`, `/talks`, `/talks.html`, `/beta/`, the custom 404, and the Atom feed remain available. GitHub Pages handles the extensionless HTML routes. Existing project websites such as `/rliable/` are separate repositories and are not modified here.

Review the `Site checks` workflow before merging. Keep **Enforce HTTPS** enabled in Pages settings. See [the security review](.github/SECURITY-REVIEW.md) for validation and hosting limitations.

## Licensing

The original site is [MIT licensed](LICENSE). Local fonts retain their respective open-font licenses in `css/fonts/`; see [font provenance](.github/FONTS.md).
