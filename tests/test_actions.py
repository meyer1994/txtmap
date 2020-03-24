from unittest import mock
from tests.base import ItemTest, ConnectionTest

from txtmap.actions import Actions
from txtmap.database import Cursor


@mock.patch.object(Actions, 'send')
class TestActions(ItemTest, ConnectionTest):
    def test_get(self, mocked):
        """ Gets a single item from DB """
        pass  # No way to test

    def test_set(self, mocked):
        """ Sets a single item into DB """
        actions = Actions(self.url)
        event = {'action': 'SET', 'x': 0, 'y': 0, 'char': 'x'}
        event = {'body': event}
        actions(event)

        sql = r'SELECT char FROM item WHERE x = 0 AND y = 0'
        with Cursor(self.url) as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
        self.assertEqual(result.char, 'x')

    def test_area(self, mocked):
        """ Gets area from DB """
        pass  # No way to test
