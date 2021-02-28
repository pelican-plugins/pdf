import locale
import logging
import os
from shutil import rmtree
from tempfile import mkdtemp
import unittest

from pelican import Pelican
from pelican.readers import MarkdownReader
from pelican.settings import read_settings

import pdf

CUR_DIR = os.path.dirname(__file__)


class TestPdfGeneration(unittest.TestCase):
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

        try:
            pelican.run()
        except ValueError:
            logging.warn(
                "Relative links in the form of "
                + "|filename|images/test.png are not yet handled by "
                + " the pdf generator"
            )
            pass

    def tearDown(self):
        rmtree(self.temp_path)
        pass

    def test_existence(self):
        assert os.path.exists(
            os.path.join(self.temp_path, "pdf", "my-super-post-rst.pdf")
        )
        if MarkdownReader.enabled:
            assert os.path.exists(
                os.path.join(self.temp_path, "pdf", "my-super-post-md.pdf")
            )
