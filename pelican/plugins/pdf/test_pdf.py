import locale
import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

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
