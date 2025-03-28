import unittest
import os

from bp_text import pdf

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

class TestPdf(unittest.TestCase):
    def setUp(self):
        """
        Set up method that runs before each test.
        Use this to initialize any objects or data needed for testing.
        """
        self.pdf1 = pdf.PdfFile(os.path.join(DATA_DIR, "bajohr2024a.pdf"))
        pass

    def test_get_lang(self):
        result = self.pdf1.lang
        self.assertEqual(result, "de")


    def test_has_data(self):
        result = type(self.pdf1.data[1].text)
        self.assertEqual(result, str)
        

    

################################################################################
## EOF test_pdf.py
