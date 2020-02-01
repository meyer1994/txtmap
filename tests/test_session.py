from unittest import TestCase

from txtmap.database import Cursor
from txtmap.textmap import TextMap

DATA = [
    'TXTMAP_0',
    'TXTMAP_1',
    'TXTMAP_2',
    'TXTMAP_3',
    'TXTMAP_4',
    'TXTMAP_5'
]


class TestTextMap(TestCase):

    def setUp(self):
        sql = r'''
        INSERT INTO item (x, y, char) VALUES (%s, %s, %s)
        '''
        with Cursor() as cursor:
            for y, line in enumerate(DATA):
                for x, char in enumerate(line):
                    values = (x, y, char)
                    cursor.execute(sql, values)

    def tearDown(self):
        # Delete table
        with Cursor() as cursor:
            cursor.execute(r'TRUNCATE TABLE item')

    def test_get(self):
        txtmap = TextMap()

        # Get point already set
        point = txtmap.get(7, 0)
        self.assertEqual(point.char, '0')

        # Get point not set
        point = txtmap.get(100, 100)
        self.assertEqual(point.char, ' ')

    def test_set(self):
        txtmap = TextMap()

        # Set point already set
        txtmap.set(0, 0, 'a')
        point = txtmap.get(0, 0)
        self.assertEqual(point.char, 'a')

        # Set point not set yet
        txtmap.set(1000, 1000, 'x')
        point = txtmap.get(1000, 1000)
        self.assertEqual(point.char, 'x')

    def test_area(self):
        txtmap = TextMap()

        width = len(DATA[0])
        height = len(DATA)

        # Fetches all input area
        area = txtmap.area(0, 0, width, height)
        self.assertEqual(len(area), 48)
        for y, line in enumerate(DATA):
            for x, char in enumerate(line):
                item = (x, y, char)
                self.assertIn(item, area)

        # Fetches area not input
        area = txtmap.area(0, 0, 100, 1)
        self.assertEqual(len(area), 100)
        for i, c in enumerate(DATA[0]):
            item = (i, 0, c)
            print(item)
            self.assertIn(item, area)
