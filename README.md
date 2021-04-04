PDF Generator: A Plugin for Pelican
===================================

[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/pdf/build)](https://github.com/pelican-plugins/pdf/actions)
[![PyPI Version](https://img.shields.io/pypi/v/pelican-pdf)](https://pypi.org/project/pelican-pdf/)
![License](https://img.shields.io/pypi/l/pelican-pdf?color=blue)

The PDF Generator plugin automatically exports articles and pages as PDF files as part of the site generation process.
PDFs are saved to: `output/pdf/`

Installation
------------

This plugin can be installed via:

    python -m pip install pelican-pdf

Usage
-----

To customize the PDF output, you can use the following settings in your Pelican configuration file:

	PDF_STYLE = ""
	PDF_STYLE_PATH = ""

`PDF_STYLE_PATH` defines a new path where *rst2pdf* will look for style sheets, while `PDF_STYLE` specifies the style you want to use.
For a description of the available styles, please read the [rst2pdf documentation](http://rst2pdf.ralsina.me/handbook.html#styles).

Known Issues
------------

Intra-site link syntax in the form of `{filename}images/test.png` is not yet handled by the PDF generator.

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
