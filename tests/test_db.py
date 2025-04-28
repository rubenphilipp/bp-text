import unittest
import os
import shutil
from pathlib import Path

from bp_text import database
from bp_text import pool

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

    def test_make_pool(self):
        dir_path = Path("/tmp/test_pool_cache")
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            
        # new cache
        result1 = self.db1.make_pool(cache="/tmp/test_pool_cache")
        # existing cache
        result2 = self.db1.make_pool(cache="/tmp/test_pool_cache")
        self.assertEqual(isinstance(result1, pool.Pool), True)
        self.assertEqual(isinstance(result2, pool.Pool), True)
        
