from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock, MagicMock

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
    async def test_coord(self, Coordinate=None):
        """ Returns a single coordinate from db """
        Coordinate.objects.create.return_value = {'x': 1, 'y': 0, 'c': 'x'}

        coord = PostCoord(x=1, y=0, c='x')
        result = await services.coord(coord)

        Coordinate.objects.create.assert_called_once_with(x=1, y=0, c='x')
        expected = {'x': 1, 'y': 0, 'c': 'x'}
        self.assertEquals(result, expected)

    @patch('txtmap.services.broadcast')
    async def test_subscribe(self, broadcast):
        """ Correctly subscribes to broadcaster """
        event = MagicMock()
        event.message = 'message'
        subscriber = MagicMock()
        subscriber.__aiter__.return_value = [event]
        context = MagicMock()
        context.__aenter__.return_value = subscriber
        broadcast.subscribe.return_value = context

        ws = AsyncMock()
        await services.subscribe(ws)

        broadcast.subscribe.assert_called_once_with(channel='map')
        subscriber.__aiter__.assert_called_once()
        ws.send_text.assert_called_once_with('message')

    async def test_publish(self, broadcast):
        pass
