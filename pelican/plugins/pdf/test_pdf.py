import locale
import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest
from unittest import mock

import docutils.core
import docutils.nodes
from rst2pdf.createpdf import RstToPdf

import pdf
from pelican import Pelican
from pelican.readers import MarkdownReader
from pelican.settings import read_settings

CUR_DIR = os.path.dirname(__file__)


def build_generator(override):
    """Return a PdfGenerator for the given settings, without running Pelican."""
    settings = read_settings(override=override)
    # The constructor writes no files, so output_path is not created
    return pdf.PdfGenerator(
        context={},
        settings=settings,
        path=os.path.join(CUR_DIR, "test_data"),
        theme=settings["THEME"],
        output_path=os.path.join(CUR_DIR, "output"),
    )


class TestPdfGeneration(unittest.TestCase):
    """Test class for PDF generation."""

    def setUp(self, override=None):
        self.temp_path = mkdtemp(prefix="pelicantests.")
        settings = {
            "PATH": os.path.join(CUR_DIR, "test_data"),
            "OUTPUT_PATH": self.temp_path,
            "PLUGINS": [pdf],
            "LOCALE": locale.normalize("en_US"),
        }
        if override:
            settings.update(override)

        self.settings = read_settings(override=settings)
        pelican = Pelican(settings=self.settings)

        pelican.run()

    def tearDown(self):
        rmtree(self.temp_path)

    def test_existence(self):
        assert os.path.exists(
            os.path.join(self.temp_path, "pdf", "my-super-post-rst.pdf")
        )
        if MarkdownReader.enabled:
            assert os.path.exists(
                os.path.join(self.temp_path, "pdf", "my-super-post-md.pdf")
            )


class TestStripElementsWithClasses(unittest.TestCase):
    """Test class for the PDF_STRIP_ELEMENTS_WITH_CLASSES setting."""

    def test_strip_elements_with_classes(self):
        cases = [
            {
                "name": "setting not set",
                "override": {},
                "expected": [],
            },
            {
                "name": "setting set",
                "override": {"PDF_STRIP_ELEMENTS_WITH_CLASSES": ["no-pdf"]},
                "expected": ["no-pdf"],
            },
        ]

        for case in cases:
            with self.subTest(case["name"]):
                generator = build_generator(case["override"])

                assert (
                    generator.pdfcreator.strip_elements_with_classes == case["expected"]
                )


class TestStripMetadata(unittest.TestCase):
    """Test class for the PDF_STRIP_METADATA setting."""

    def test_strip_metadata(self):
        temp_path = mkdtemp(prefix="pelicantests.")
        self.addCleanup(rmtree, temp_path)
        settings = {
            "PATH": os.path.join(CUR_DIR, "test_data"),
            "OUTPUT_PATH": temp_path,
            "PLUGINS": [pdf],
            "LOCALE": locale.normalize("en_US"),
            "PDF_STRIP_METADATA": True,
        }
        pelican = Pelican(settings=read_settings(override=settings))
        create_pdf = RstToPdf.createPdf

        # Record the calls, but still run the real createPdf
        with mock.patch.object(
            RstToPdf, "createPdf", autospec=True, side_effect=create_pdf
        ) as create_pdf_mock:
            pelican.run()

        assert create_pdf_mock.call_count > 0
        for call in create_pdf_mock.call_args_list:
            doctree = call.kwargs["doctree"]
            assert doctree.next_node(docutils.nodes.docinfo) is None


class TestParseDoctree(unittest.TestCase):
    """Test class for _parse_doctree and its error handling."""

    def test_parse_doctree(self):
        cases = [
            {
                "name": "valid text",
                "text": "Title\n=====\n\nText.\n",
                "exception": None,
                "expect_doctree": True,
            },
            {
                "name": "invalid text",
                "text": ".. unknown-directive::\n",
                "exception": None,
                "expect_doctree": False,
            },
            {
                "name": "exception other than a docutils SystemMessage",
                "text": "Text.\n",
                "exception": ValueError("parse failed"),
                "expect_doctree": False,
            },
        ]

        generator = build_generator({"PDF_STRIP_ELEMENTS_WITH_CLASSES": ["no-pdf"]})

        for case in cases:
            with self.subTest(case["name"]):
                if case["exception"] is None:
                    doctree = generator._parse_doctree(case["text"])
                else:
                    with mock.patch.object(
                        docutils.core, "publish_doctree", side_effect=case["exception"]
                    ):
                        doctree = generator._parse_doctree(case["text"])

                if case["expect_doctree"]:
                    # rst2pdf reads the classes to strip from the doctree settings
                    assert doctree.settings.strip_elements_with_classes == ["no-pdf"]
                else:
                    assert doctree is None

    def test_failed_parse_writes_no_pdf(self):
        temp_path = mkdtemp(prefix="pelicantests.")
        self.addCleanup(rmtree, temp_path)
        settings = {
            "PATH": os.path.join(CUR_DIR, "test_data"),
            "OUTPUT_PATH": temp_path,
            "PLUGINS": [pdf],
            "LOCALE": locale.normalize("en_US"),
            "PDF_STRIP_METADATA": True,
        }
        pelican = Pelican(settings=read_settings(override=settings))

        # The test data is valid, so we let the parsing fail
        with mock.patch.object(pdf.PdfGenerator, "_parse_doctree", return_value=None):
            pelican.run()

        assert os.listdir(os.path.join(temp_path, "pdf")) == []
