from unittest.mock import patch, AsyncMock
from unittest import IsolatedAsyncioTestCase

from txtmap import services
from txtmap.models import PostArea, PostCoord


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
        area = PostArea(a=a, b=b)
        result = await services.area(area)

        database.fetch_all.assert_called_once()
        self.assertEquals(len(result), 3)
        for item in values:
            self.assertIn(item, result)

    @patch('txtmap.services.Coordinate', new_callable=AsyncMock)
    async def test_coord(self, Coordinate):
        """ Returns a single coordinate from db """
        Coordinate.objects.create.return_value = {'x': 1, 'y': 0, 'c': 'x'}

        coord = PostCoord(x=1, y=0, c='x')
        result = await services.coord(coord)

        Coordinate.objects.create.assert_called_once_with(x=1, y=0, c='x')
        expected = {'x': 1, 'y': 0, 'c': 'x'}
        self.assertEquals(result, expected)

    async def test_publish(self):
        pass

    async def test_subscribe(self):
        pass
