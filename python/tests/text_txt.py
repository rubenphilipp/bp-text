import unittest
import os

from bp_text import txt

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

class TestTxt(unittest.TestCase):
    def setUp(self):
        """
        Set up method that runs before each test.
        Use this to initialize any objects or data needed for testing.
        """
        self.txt1 = txt.TxtFile(os.path.join(DATA_DIR, "nietzsche 1.txt"))
        pass

    def test_get_lang(self):
        result = self.txt1.lang
        self.assertEqual(result, 'de')
        
