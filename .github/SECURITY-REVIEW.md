# Security and functionality review — 2026-09-19

## Scope

Reviewed the checked-out website, its templates, browser dependencies, public response headers, accessible GitHub Pages settings, local resources, and external links. This is a scoped source and browser review, not a guarantee that every vulnerability has been found. Project sites hosted from other repositories under the same origin are outside this change.

## Fixed

- Removed jQuery 3.1.1, Slideout, old Distill/MathJax/webcomponents loaders, unused bundled JavaScript, and all execution paths for third-party scripts. These were unnecessary for the static content; no replacement framework is introduced.
- Removed Google Analytics, CDN icon/font styles, external fonts, YouTube iframes, and SlidesLive embeds. Recordings remain ordinary HTTPS links, and local research figures replace embedded players.
- Added an early CSP on every HTML page, including the 404 and legacy `/beta/` redirect. It denies scripts, frames, network connections, objects, form submissions, and base URL overrides; permits only same-origin CSS and images; and requests upgrades of insecure resources. No inline styles or `unsafe-inline` exceptions.
- Added `no-referrer` to all pages. External links use the same tab, so there is no new-window opener relationship. Regression checks require `noopener noreferrer` if new-tab links are added.
- Removed the unbounded Ruby/Jekyll dependency chain, stale templates, and notebook conversion hooks. Plain HTML is published using `.nojekyll`; an optional standard-library Python renderer maintains shared layout. No package installation is needed to render or check the site.
- Added a read-only CI workflow with a SHA-pinned checkout action, no persisted checkout credentials, and a five-minute timeout; Dependabot maintains the Actions dependency.
- Fixed malformed markup, missing image descriptions/dimensions, missing favicon, an incorrectly relative project link, HTTP project links, stale Google Brain page titles, and invalid feed/site URLs. Preserved 19 visible research entries and the public content.
- Removed three broken archival destinations while preserving their talk entries: Edinburgh reading-group and BlueJeans hosts did not resolve; the 2020 ML Collective slides returned 404.
- Refreshed responsive styling, semantic heading hierarchy, visible keyboard focus, skip navigation, native mobile navigation, light/dark colors, and 404 recovery links.

## Validation

- Standard-library validator checks every published HTML page, strict CSP, disallowed active content, markup nesting, duplicate IDs, image metadata, internal anchors, local resources, and feed/sitemap/favicon XML.
- Five regression tests include eleven hostile markup cases, a weakened CSP, missing referrer protection, and malformed HTML. All pass.
- All 92 unique external links were requested before cleanup: 87 returned successful responses, three broken destinations were removed, LinkedIn returned anti-bot status 999, and ServiceNow returned 403. Successful status codes do not establish that a destination remains publicly usable; some providers return sign-in or challenge pages.
- Pattern scan of all 367 unique blobs in reachable Git history found no matches for private keys or common GitHub, AWS, Google API, or Slack token formats. This limited scan cannot rule out arbitrary secrets.
- Browser verification: desktop and narrow layouts, all 19 publication entries, native navigation, no script/iframe elements or external subresources, no console errors, and custom 404 recovery. Local HTTP checks return 200 for `/research`, `/talks`, and `/beta/`, and 404 for missing pages.
- Live Pages API confirms `https_enforced: true`, source `master` at `/`, and no custom domain.

## Hosting and account limitations

The existing hosting is GitHub Pages. This repository cannot configure arbitrary HTTP response headers there. The live root response did not include CSP, HSTS, `X-Content-Type-Options`, a frame restriction, or Permissions-Policy. The HTML meta CSP supplies supported document protections after deployment, but **`frame-ancestors` cannot be enforced through a meta tag**. No fake `_headers` file or ineffective meta header substitutes are included.

If framing protection and additional HTTP headers are required, use a hosting service or reverse proxy that supports response headers, then set a header-based CSP including `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, and an appropriate Permissions-Policy. Configure HSTS only after verifying HTTPS for every hostname covered by its policy. A hosting migration or domain change is not part of this patch.

The CLI/connector account `rishabh_per` is read-only and cannot fork this public repository under its Enterprise Managed User policy. The owner subsequently provided their existing `agarwl` Chrome session. The owner-visible Dependabot page reports **0 open / 0 closed alerts**. This does not establish that legacy scripts loaded directly from CDNs were safe or fully inventoried.

Through the owner session, private vulnerability reporting and Dependabot malware alerts were enabled and verified. Dependency graph, Dependabot alerts, and automatic security updates were already enabled. Secret Protection was enabled with explicit user approval; its alert page currently reports 0 open / 0 closed alerts and no unresolved secrets. Push protection is a separate setting and remains pending explicit approval. Branch protections and CodeQL setup have not been changed. The code changes remain local until publishing is completed.
