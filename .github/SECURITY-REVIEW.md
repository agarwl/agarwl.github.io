# Security review — 2026-09-19

## Scope

Reviewed this website’s source, templates, browser dependencies, reachable Git history, public response headers, GitHub Pages settings, security alerts, local resources, and external links. The existing site structure, typography, colors, content order, and biography are preserved, with small spacing and mobile wrapping refinements. This is a scoped review, not a guarantee that every vulnerability has been found. Project websites hosted from other repositories under the same origin are outside this change.

## Code changes

- Removed jQuery 3.1.1, Slideout, old Distill/MathJax/webcomponents loaders, unused JavaScript bundles, and execution paths for third-party scripts. The existing hamburger menu now uses native HTML disclosure controls with the same navigation links.
- Removed Google Analytics and embedded YouTube/SlidesLive players. Existing recordings remain available as links; local research figures occupy the original media columns.
- Preserved Fira Sans, Raleway, Font Awesome, and Academicons using local font files and local CSS. Removed font/icon CDN requests, the remote stylesheet import, and references to missing EOT/icon assets. Font licenses and SHA-256 provenance are included.
- Added an early Content Security Policy on every HTML page, including the 404 and legacy `/beta/` redirect. It denies scripts, frames, network connections, objects, form submissions, and base URL overrides; permits only same-origin stylesheets, images, and fonts; and requests upgrades of insecure resources. No inline styles or `unsafe-inline` exceptions are needed.
- Added `no-referrer` to all pages and `noopener noreferrer` to existing new-tab links. Preserved their original tab-opening behavior.
- Removed the unbounded Ruby/Jekyll dependency chain, unused templates, and notebook conversion hooks. Plain HTML is published using `.nojekyll`; a standard-library Python renderer maintains the shared layout. Rendering and validation require no downloaded packages.
- Added a read-only CI workflow with a SHA-pinned checkout action, no persisted checkout credentials, and a five-minute timeout. Dependabot monitors the Actions dependency.
- Tightened header spacing, improved list readability and footer wrapping, and made research-link rows wrap on narrow screens without changing the desktop columns.
- Fixed malformed HTML, missing image descriptions/dimensions, missing favicon, an incorrectly relative project link, HTTP project links, stale Google Brain page titles, invalid feed/site URLs, and stylesheet cache invalidation.
- Removed three broken archival destinations while keeping their talk entries: the Edinburgh reading-group and BlueJeans hosts did not resolve; the 2020 ML Collective slides returned 404.

## Validation

- Every published HTML page passes offline checks for CSP, disallowed active content, markup nesting, duplicate IDs, image metadata, internal anchors, local resources, local-only font URLs, and feed/sitemap/favicon XML.
- Six regression tests cover eleven hostile markup cases, escaped and remote CSS URLs, a weakened CSP, missing referrer protection, and malformed HTML.
- Browser checks confirm the original desktop layout, a working native mobile menu at 320px and 390px, no horizontal overflow on the homepage or research page at those widths, all 19 visible research entries, no broken loaded images, no script/iframe elements, and no console errors.
- Local HTTP checks return 200 for `/research`, `/talks`, and `/beta/`, and 404 for missing pages. The `/beta/` redirect was also checked in the browser.
- All 92 unique external links were requested before cleanup: 87 returned successful responses, three broken destinations were removed, LinkedIn returned anti-bot status 999, and ServiceNow returned 403. Successful status codes do not establish that a destination remains publicly usable; some providers return sign-in or challenge pages.
- Pattern scanning all 367 unique blobs in reachable Git history found no matches for private keys or common GitHub, AWS, Google API, or Slack token formats. This limited scan cannot rule out arbitrary secrets.

## Verified repository settings

The owner account confirmed HTTPS enforcement is enabled, with Pages serving the `master` branch at `/` and no custom domain. Dependabot shows 0 open and 0 closed alerts; this does not establish that scripts loaded directly from CDNs were fully inventoried.

Private vulnerability reporting, Dependabot malware alerts, and Secret Protection were enabled. Secret scanning currently reports 0 open and 0 closed alerts with no unresolved secrets. Dependency graph, Dependabot alerts, and automatic security updates were already enabled. Push protection remains disabled at the owner’s explicit request. The default branch is not protected. Branch protections and CodeQL setup were not changed; the owner can require the Site checks check after its first successful run.

## Hosting limitations

GitHub Pages does not let this repository configure arbitrary HTTP response headers. The live root response inspected before this change did not include CSP, HSTS, `X-Content-Type-Options`, a frame restriction, or Permissions-Policy. The HTML meta CSP supplies supported document protections after deployment, but **`frame-ancestors` cannot be enforced through a meta tag**. No ineffective `_headers` file or meta substitutes for header-only controls are included.

Header-based framing protection and additional HTTP headers require a hosting service or reverse proxy with response-header support. A suitable header-based CSP should include `frame-ancestors 'none'`; other useful headers include `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and a restrictive Permissions-Policy. Configure HSTS only after verifying HTTPS for every hostname covered by it. This patch does not migrate hosting or change domains.
