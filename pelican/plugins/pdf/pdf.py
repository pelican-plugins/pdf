"""PDF Generator plugin for Pelican.

This plugin generates PDF files from reStructuredText and Markdown source files.
"""

from itertools import chain
import logging
import os
import re
import time

from rst2pdf.createpdf import RstToPdf

from pelican import signals
from pelican.generators import Generator
from pelican.readers import MarkdownReader

logger = logging.getLogger(__name__)


class PdfGenerator(Generator):
    """Generate PDFs on the output dir, for all articles and pages."""

    supported_md_fields = ["date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "PDF_STYLE_PATH" in self.settings:
            pdf_style_path = [self.settings["PDF_STYLE_PATH"]]
        else:
            pdf_style_path = []

        pdf_style = [self.settings["PDF_STYLE"]] if "PDF_STYLE" in self.settings else []

        self.pdfcreator = RstToPdf(
            breakside=0, stylesheets=pdf_style, style_path=pdf_style_path, raw_html=True
        )

    def _create_pdf(self, obj, output_path):
        filename = obj.slug + ".pdf"
        output_pdf = os.path.join(output_path, filename)
        mdreader = MarkdownReader(self.settings)
        _, ext = os.path.splitext(obj.source_path)

        if ext == ".rst":
            with open(obj.source_path, encoding="utf-8") as f:
                text = f.read()

            header = ""

            # Use full path for images to avoid rst2pdf 'Missing image file' error
            # Match reStructuredText Syntax: ..image:: {static}/images/picture.jpg
            text = re.sub(r"(\.\. image:: )({.*})", r"\1" + self.path, text)

        elif ext[1:] in mdreader.file_extensions and mdreader.enabled:
            text, meta = mdreader.read(obj.source_path)
            header = ""

            if "title" in meta:
                title = meta["title"]
                header = title + "\n" + "#" * len(title) + "\n\n"
                del meta["title"]

            for k in list(meta):
                # We can't support all fields, so we strip the ones that won't
                # look good
                if k not in self.supported_md_fields:
                    del meta[k]

            header += "\n".join([f":{k}: {meta[k]}" for k in meta])
            header += "\n\n.. raw:: html\n\n\t"
            text = text.replace("\n", "\n\t")

            # rst2pdf casts the text to str and will break if it finds
            # non-escaped characters. Here we nicely escape them to XML/HTML
            # entities before proceeding
            text = text.encode("ascii", "xmlcharrefreplace").decode()

            # Use full path for images to avoid rst2pdf 'Missing image file' error
            # Match Markdown Syntax: ![alt]({static}/images/picture.jpg)
            text = re.sub(r"(!\[.*\]\()({.*})", r"\1" + self.path, text)

        else:
            # We don't support this format
            logger.warn("Ignoring unsupported file " + obj.source_path)
            return

        # Find intra-site links and replace placeholder with actual path / url
        hrefs = self._get_intrasite_link_regex()
        text = hrefs.sub(lambda m: obj._link_replacer(obj.get_siteurl(), m), text)

        logger.info(f" [ok] writing {output_pdf}")

        self.pdfcreator.createPdf(text=(header + text), output=output_pdf)

        if obj.date is not None:
            self._set_file_utime(output_pdf, obj.date)

    def _get_intrasite_link_regex(self):
        intrasite_link_regex = self.settings["INTRASITE_LINK_REGEX"]
        regex = rf"""
                (?P<markup>)(?P<quote>)(?P<path>(\:?){intrasite_link_regex}(?P<value>.*?)(?=[>\n]))
                """
        return re.compile(regex, re.X)

    def _set_file_utime(self, path, datetime):
        """Set modified time (mtime) of specified file."""
        mtime = time.mktime(datetime.timetuple())
        os.utime(path, (mtime, mtime))

    def generate_context(self):
        pass

    def generate_output(self, writer=None):
        # we don't use the writer passed as argument here
        # since we write our own files
        logger.info(" Generating PDF files...")
        pdf_path = os.path.join(self.output_path, "pdf")
        if not os.path.exists(pdf_path):
            try:
                os.mkdir(pdf_path)
            except OSError:
                logger.exception("Couldn't create the pdf output folder in " + pdf_path)

        for obj in chain(self.context["articles"], self.context["pages"]):
            self._create_pdf(obj, pdf_path)
            for obj_trans in obj.translations:
                self._create_pdf(obj_trans, pdf_path)


def get_generators(generators):
    return PdfGenerator


def register():
    signals.get_generators.connect(get_generators)
