from txtmap.database import Connections, Cursor

from tests.base import ConnectionTest


class TestConnections(ConnectionTest):
    def test_add(self):
        conn = Connections(self.url)
        _id = 'some_id'

        conn.add(_id)

        sql = r'SELECT count(id) AS count FROM connection WHERE id = %s'
        value = (_id, )
        with Cursor(self.url) as cursor:
            cursor.execute(sql, value)
            result = cursor.fetchone()

        self.assertEqual(result.count, 1)

    def test_remove(self):
        conn = Connections(self.url)
        result = conn.remove('id_0')
        self.assertEqual(result, 'id_0')

        sql = r'SELECT count(id) AS count FROM connection'
        with Cursor(self.url) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()

        self.assertEqual(result.count, 7)

    def test_all(self):
        conn = Connections(self.url)
        result = conn.all()
        self.assertListEqual(result, self.DATA)
