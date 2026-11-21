PDF Generator: A Plugin for Pelican
===================================

[![Build Status](https://img.shields.io/github/actions/workflow/status/pelican-plugins/pdf/main.yml?branch=main)](https://github.com/pelican-plugins/pdf/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-pdf)](https://pypi.org/project/pelican-pdf/)
[![Downloads](https://img.shields.io/pypi/dm/pelican-pdf)](https://pypi.org/project/pelican-pdf/)
![License](https://img.shields.io/pypi/l/pelican-pdf?color=blue)

The PDF Generator plugin automatically exports articles and pages as PDF files as part of the site generation process.
PDFs are saved to: `output/pdf/`

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-pdf

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `pdf` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

Usage
-----

To customize the PDF output, you can use the following settings in your Pelican configuration file:

	PDF_STYLE = ""
	PDF_STYLE_PATH = ""
	PDF_STRIP_ELEMENTS_WITH_CLASSES = []
	PDF_STRIP_METADATA = False
	PDF_DATE_FORMAT = None

`PDF_STYLE_PATH` defines a new path where *rst2pdf* will look for style sheets, while `PDF_STYLE` specifies the style you want to use.
For a description of the available styles, please read the [rst2pdf documentation](https://rst2pdf.org/manual.html#creating-stylesheets).

`PDF_STRIP_ELEMENTS_WITH_CLASSES` removes all elements with one of the listed classes from the PDF.
For example, with `PDF_STRIP_ELEMENTS_WITH_CLASSES = ["no-pdf"]`, the table of contents and the paragraph below are not part of the PDF:

	.. contents::
	   :class: no-pdf

	.. class:: no-pdf

	This paragraph is not part of the PDF.

`PDF_STRIP_METADATA` removes the metadata fields (`:date:`, `:slug:`, `:tags:` and so on) from the top of the PDF.
It applies to reStructuredText and Markdown files.

Page headers and footers are defined in your `PDF_STYLE` style sheet, with `defaultHeader` and `defaultFooter` in the [page templates](https://rst2pdf.org/manual.html#page-templates).
They accept reStructuredText and the *rst2pdf* [placeholders](https://rst2pdf.org/manual.html#headers-and-footers) like `###Title###`, `###Page###` and `###Total###`.
If a document uses the `.. header::` or `.. footer::` directive, they are used instead.

The plugin adds the substitution `|pdf_updated|` to every article and page, so you can use it in headers and footers.
It is replaced with the `modified` date of the article or page.
If no `modified` date is set, the `date` is used, and if neither is set, it is replaced with an empty string.

`PDF_DATE_FORMAT` specifies the date format of `|pdf_updated|`, for example `"%Y-%m-%d"`, and falls back to the Pelican date format of the article or page if it is not set.

	pageTemplates:
	  mainPage:
	    defaultHeader: |
	      .. class:: header

	      ###Title###
	    defaultFooter: |
	      .. class:: footer

	      Last updated: |pdf_updated| | Page ###Page### of ###Total###

The `header` and `footer` classes give the text the same style as the `.. header::` and `.. footer::` directives.
`mainPage` is the default first page template.
If your documents switch to other page templates, set `defaultHeader` and `defaultFooter` there too.

Contributors
------------

Contributors include: Dominik Wombacher, Justin Mayer, Kyle Mahan, Renato Cunha, dpetzel, and Lucas Cimon

Contributing
------------

Contributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].

To start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.

[existing issues]: https://github.com/pelican-plugins/pdf/issues
[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html

License
-------

This project is licensed under the AGPL 3.0 license.
