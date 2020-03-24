from unittest import TestCase

from txtmap.database import Cursor


class BaseTest(TestCase):
    url = 'postgresql://postgres:@localhost:5432/postgres'


class ConnectionTest(BaseTest):
    DATA = ['id_0', 'id_1', 'id_2', 'id_3', 'id_4', 'id_5', 'id_6', 'id_7']

    def setUp(self):
        """ Inserts data into table `connection` """
        super().setUp()
        sql = r'INSERT INTO connection (id) VALUES (%s)'
        with Cursor(self.url) as cursor:
            for item in self.DATA:
                value = (item, )
                cursor.execute(sql, value)

    def tearDown(self):
        """ Truncates table `connection` """
        super().tearDown()
        sql = r'TRUNCATE TABLE connection'
        with Cursor(self.url) as cursor:
            cursor.execute(sql)


class ItemTest(BaseTest):
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

    def setUp(self):
        """ Inserts data into table `item` """
        super().setUp()
        sql = r'INSERT INTO item (x, y, char) VALUES (%s, %s, %s)'
        with Cursor(self.url) as cursor:
            for y, line in enumerate(self.DATA):
                for x, char in enumerate(line):
                    values = (x, y, char)
                    cursor.execute(sql, values)

    def tearDown(self):
        """ Truncates table `item` """
        super().tearDown()
        sql = r'TRUNCATE TABLE item'
        with Cursor(self.url) as cursor:
            cursor.execute(sql)
