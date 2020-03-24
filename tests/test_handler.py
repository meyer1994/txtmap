from unittest import mock
from tests.base import ConnectionTest

from txtmap.handler import Handler
from txtmap.actions import Actions
from txtmap.database import Cursor


class TestHanlder(ConnectionTest):
    def test_disconnect(self):
        """ Removes connection to DB """
        handler = Handler(self.url)
        event = {'eventType': 'DISCONNECT', 'connectionId': 'myid'}
        event = {'requestContext': event}
        handler(event, None)

        sql = r'SELECT count(id) FROM connection WHERE id = %s'
        data = ('myid', )
        with Cursor(self.url) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
        self.assertEqual(result.count, 0)

    def test_connect(self):
        """ Adds connection to DB """
        handler = Handler(self.url)
        event = {'eventType': 'CONNECT', 'connectionId': 'myid'}
        event = {'requestContext': event}
        handler(event, None)

        sql = r'SELECT count(id) FROM connection WHERE id = %s'
        data = ('myid', )
        with Cursor(self.url) as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()
        self.assertEqual(result.count, 1)

    @mock.patch.object(Actions, '__call__')
    def test_default(self, mocked):
        """ Processes a message """
        handler = Handler(self.url)
        event = {'eventType': 'MESSAGE', 'connectionId': 'myid'}
        event = {'requestContext': event, 'body': '[]'}
        handler(event, None)

        mocked.assert_called_once()
