import unittest
from src.database import Database
from src.queries import get_all_records

class TestSQLiteExamples(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Database('test_database.db')
        cls.db.create_table('test_table', {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})
        cls.db.insert('test_table', {'name': 'Alice'})
        cls.db.insert('test_table', {'name': 'Bob'})

    def test_get_all_records(self):
        records = get_all_records('test_table')
        self.assertEqual(len(records), 2)
        self.assertIn(('Alice',), records)
        self.assertIn(('Bob',), records)

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_table('test_table')
        cls.db.close()

if __name__ == '__main__':
    unittest.main()