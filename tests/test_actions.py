from unittest import mock
from tests.base import ItemTest, ConnectionTest

from txtmap.actions import Actions
from txtmap.database import Cursor


@mock.patch.object(Actions, '_send')
class TestActions(ItemTest, ConnectionTest):
    def event(self, action, x, y, char, _id):
        return {
            'body': {'action': action, 'x': x, 'y': y, 'char': char},
            'requestContext': {'connectionId': _id}
        }

    def test_get(self, mocked):
        """ Gets a single item from DB """
        actions = Actions(self.url)
        event = self.event('GET', 0, 0, None, 'id_0')
        actions(event)

        mocked.assert_called_once_with(event, [(0, 0, 'T')], ['id_0'])

    def test_set(self, mocked):
        """ Sets a single item into DB """
        actions = Actions(self.url)
        event = self.event('SET', 0, 0, 'x', 'id_0')
        actions(event)

        sql = r'SELECT char FROM item WHERE x = 0 AND y = 0'
        with Cursor(self.url) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        self.assertEqual(result.char, 'x')

    def test_area(self, mocked):
        """ Gets area from DB """
        actions = Actions(self.url)
        event = self.event('AREA', 0, 0, None, 'id_0')
        event['body']['width'] = 1
        event['body']['heigth'] = 1
        actions(event)

        mocked.assert_called_once_with(event, [(0, 0, 'T')], ['id_0'])
