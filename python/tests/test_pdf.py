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
        self.pdf1 = pdf.PdfFile(os.path.join(DATA_DIR, "bajohr2024a_s.pdf"),
                                tagger_ner=False)
        ## contains roman numerals on some pages
        self.pdf2 = pdf.PdfFile(
            os.path.join(DATA_DIR, "Infrastructure_Aesthetics_2024.pdf"),
            tagger_pos = False,
            tagger_ner = False)
        pass

    def test_get_lang(self):
        result = self.pdf1.lang
        self.assertEqual(result, "de")


    def test_has_data(self):
        result = type(self.pdf1.data[1].raw_text)
        self.assertEqual(result, str)

    def test_no_auto_extract(self):
        result = pdf.PdfFile(os.path.join(DATA_DIR, "bajohr2024a_s.pdf"),
                             auto_extract = False,
                             tagger_ner = False)
        self.assertEqual(isinstance(result, pdf.PdfFile), True)
        
    def text_page_labels(self):
        self.assertEqual(self.pdf2.data[0].page_label, "I")
        self.assertEqual(self.pdf2.data[8].page_label, "1")
    

################################################################################
## EOF test_pdf.py
