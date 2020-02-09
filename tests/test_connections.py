from unittest import TestCase

from txtmap.database import Connections, Cursor

# Base values for docker image and travis
DB_USER = 'postgres'
DB_PASS = ''
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'

URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


DATA = [
    'id_0',
    'id_1',
    'id_2',
    'id_3',
    'id_4',
    'id_5',
    'id_6',
    'id_7'
]


class TestItems(TestCase):

    def setUp(self):
        sql = r'INSERT INTO connection (id) VALUES (%s)'

        with Cursor(URL) as cursor:
            for item in DATA:
                value = (item, )
                cursor.execute(sql, value)

    def tearDown(self):
        # Delete table
        sql = r'TRUNCATE TABLE connection'

        with Cursor(URL) as cursor:
            cursor.execute(sql)

    def test_add(self):
        conn = Connections(URL)
        _id = 'some_id'

        conn.add(_id)

        sql = r'SELECT count(id) AS count FROM connection WHERE id = %s'
        value = (_id, )
        with Cursor(URL) as cursor:
            cursor.execute(sql, value)
            result = cursor.fetchone()

        self.assertEqual(result.count, 1)

    def test_remove(self):
        conn = Connections(URL)
        result = conn.remove('id_0')
        self.assertEqual(result, 'id_0')

        sql = r'SELECT count(id) AS count FROM connection'
        with Cursor(URL) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()

        self.assertEqual(result.count, 7)

    def test_all(self):
        conn = Connections(URL)
        result = conn.all()
        self.assertListEqual(result, DATA)
