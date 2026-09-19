# Security policy

This repository publishes static HTML, CSS, and research assets. It has no login, server-side application, form submission, browser scripting, or runtime package dependencies.

Report a suspected security problem using [GitHub private vulnerability reporting](https://github.com/agarwl/agarwl.github.io/security/advisories/new) or email **rishabhagarwal.467@gmail.com**. Include the affected URL, reproduction steps, and impact. Do not post credentials or private data in a public issue.

The site’s own HTML must retain its restrictive Content Security Policy, use only local CSS and images, and must not load JavaScript, tracking pixels, external fonts, or embedded players. Link to videos and interactive external resources instead. CI enforces this baseline; the policy does not protect separate project repositories or external links after navigation.

The GitHub Actions dependency is pinned to a commit and monitored by Dependabot. Keep the supported Python runtime and action pin updated.
