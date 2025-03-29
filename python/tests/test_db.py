import unittest
import os

from bp_text import database

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, 'data')

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """
        Set up method that runs before each test.
        Use this to initialize any objects or data needed for testing.
        """
        self.db1 = database.BibTexDatabase(os.path.join(DATA_DIR,
                                                        "sources.bib"))
        pass

    def test_db(self):
        self.assertEqual(type(self.db1), database.BibTexDatabase)

    def test_file_split(self):
        result = self.db1.entries["pfeifer2003"].get("file").value
        self.assertEqual(len(result), 2)
