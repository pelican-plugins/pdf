CHANGELOG
=========

1.0.5 - 2024-09-11
------------------

Remove upper bound on `xhtml2pdf` version

1.0.4 - 2024-05-28
------------------

- Test PDF generation via GitHub CI action (#18)
- Pin `xhtml2pdf` until import from `rst2pdf` is fixed (#19)
- Replace Poetry with PDM
- Replace various code style linters with Ruff

Contributed by [Justin Mayer](https://github.com/justinmayer) via [PR #19](https://github.com/pelican-plugins/pdf/pull/19/)


1.0.3 - 2023-07-03
------------------

* Only generate PDFs when corresponding articles have changed ([#14](https://github.com/pelican-plugins/pdf/pull/14))
* Remove now-unnecessary xhtml2pdf / rst2pdf workaround ([#13](https://github.com/pelican-plugins/pdf/pull/13))

1.0.2 - 2023-04-04
------------------

Use full path for images to avoid rst2pdf “Missing image file” error ([#7](https://github.com/pelican-plugins/pdf/pull/7))

Contributed by [Dominik Wombacher](https://github.com/wombelix) via [PR #7](https://github.com/pelican-plugins/pdf/pull/7/)


1.0.1 - 2021-06-27
------------------

Support intra-site links to source content files

Contributed by [Dominik Wombacher](https://github.com/wombelix) [PR #3](https://github.com/pelican-plugins/pdf/pull/3/)


1.0.0 - 2021-04-04
------------------

Initial release as namespace plugin
