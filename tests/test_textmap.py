from unittest import TestCase

from txtmap.database import TextMap, Cursor

# Base values for docker image and travis
DB_USER = 'postgres'
DB_PASS = ''
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


DATA = [
    'TXTMAP_0',
    'TX      ',
    'T T     ',
    'T  M    ',
    'T   A   ',
    'T    P  ',
    'T     _ ',
    'T      7'
]


class TestItems(TestCase):

    def setUp(self):
        sql = r'INSERT INTO item (x, y, char) VALUES (%s, %s, %s)'

        with Cursor(URL) as cursor:
            for y, line in enumerate(DATA):
                for x, char in enumerate(line):
                    values = (x, y, char)
                    cursor.execute(sql, values)

    def tearDown(self):
        # Delete table
        sql = r'TRUNCATE TABLE item'

        with Cursor(URL) as cursor:
            cursor.execute(sql)

    def test_get(self):
        db = TextMap(URL)

        # Get point already set
        point = db.get(7, 0)
        self.assertEqual(point.char, '0')

        # Get point not set
        point = db.get(100, 100)
        self.assertIs(point.char, ' ')

    def test_set(self):
        db = TextMap(URL)

        # Update point
        point = db.get(0, 0)
        self.assertEqual(point.char, 'T')
        db.set(0, 0, 'a')
        point = db.get(0, 0)
        self.assertEqual(point.char, 'a')

        # Set point not set yet
        db.set(1000, 1000, 'x')
        point = db.get(1000, 1000)
        self.assertEqual(point.char, 'x')

    def test_area_column(self):
        db = TextMap(URL)

        # First column
        width = 1
        height = 8

        area = db.area(0, 0, width, height)
        result = ''.join(i.char for i in area)
        expected = 'TTTTTTTT'
        self.assertEqual(result, expected)

    def test_area_row(self):
        db = TextMap(URL)

        # Last row
        width = 8
        height = 1

        area = db.area(0, 7, width, height)
        result = ''.join(i.char for i in area)
        expected = 'T      7'
        self.assertEqual(result, expected)

    def test_area_set(self):
        db = TextMap(URL)

        width = 2
        height = 2

        # Fetches 2x2 area
        area = db.area(0, 0, width, height)

        result = {(x, y): c for x, y, c in area}
        expected = {
            (0, 0): 'T',
            (1, 0): 'X',
            (1, 1): 'X',
            (0, 1): 'T'
        }
        self.assertDictEqual(result, expected)

    def test_area_not_set(self):
        db = TextMap(URL)

        width = 100
        height = 100

        area = db.area(30, 30, width, height)
        result = ''.join(i.char for i in area)
        expected = ' ' * width * height
        self.assertEqual(result, expected)
