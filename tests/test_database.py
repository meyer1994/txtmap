from unittest import TestCase

from txtmap.database import Database, Cursor

DB_USER = 'postgres'
DB_PASS = ''
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


DATA = [
    'TXTMAP_0',
    'TXTMAP_1',
    'TXTMAP_2',
    'TXTMAP_3',
    'TXTMAP_4',
    'TXTMAP_5'
]


class TestDatabase(TestCase):

    def setUp(self):
        sql = r'''
        INSERT INTO item (x, y, char) VALUES (%s, %s, %s)
        '''
        with Cursor(URL) as cursor:
            for y, line in enumerate(DATA):
                for x, char in enumerate(line):
                    values = (x, y, char)
                    cursor.execute(sql, values)

    def tearDown(self):
        # Delete table
        with Cursor(URL) as cursor:
            cursor.execute(r'TRUNCATE TABLE item')

    def test_get(self):
        db = Database(URL)

        # Get point already set
        point = db.get(7, 0)
        self.assertEqual(point.char, '0')

        # Get point not set
        point = db.get(100, 100)
        self.assertEqual(point.char, ' ')

    def test_set(self):
        db = Database(URL)

        # Set point already set
        db.set(0, 0, 'a')
        point = db.get(0, 0)
        self.assertEqual(point.char, 'a')

        # Set point not set yet
        db.set(1000, 1000, 'x')
        point = db.get(1000, 1000)
        self.assertEqual(point.char, 'x')

    def test_area(self):
        db = Database(URL)

        width = len(DATA[0])
        height = len(DATA)

        # Fetches all input area
        area = db.area(0, 0, width, height)
        self.assertEqual(len(area), 48)
        for y, line in enumerate(DATA):
            for x, char in enumerate(line):
                item = (x, y, char)
                self.assertIn(item, area)

        # Fetches area not input
        area = db.area(0, 0, 100, 1)
        self.assertEqual(len(area), 100)
        for i, c in enumerate(DATA[0]):
            item = (i, 0, c)
            print(item)
            self.assertIn(item, area)
