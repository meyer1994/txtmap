from unittest.mock import patch
from unittest import IsolatedAsyncioTestCase

from txtmap import services


class TestService(IsolatedAsyncioTestCase):
    @patch('txtmap.services.database')
    async def test_area(self, database):
        """ Returns a list of coordinates from db """
        values = [
            {'x': 0, 'y': 1, 'c': 'x'},
            {'x': 1, 'y': 0, 'c': 'x'},
            {'x': 10, 'y': 10, 'c': 'x'}
        ]
        database.fetch_all.return_value = values

        a = (0, 0)
        b = (10, 10)
        result = await services.area(a, b)

        database.fetch_all.assert_called_once()

        self.assertEquals(len(result), 3)
        for item in values:
            self.assertIn(item, result)

    async def test_coord(self):
        """ Returns a single coordinate from db """
        result = await services.coord(1, 0)
        expected = {'x': 1, 'y': 0, 'c': 'x'}
        self.assertEquals(result, expected)

    async def test_publish(self):
        pass

    async def test_subscribe(self):
        pass
