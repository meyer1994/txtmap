from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from txtmap import controller
from txtmap.models import PostArea, PostCoord


class TestController(IsolatedAsyncioTestCase):

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_area(self, services):
        """ Calls `area` service """
        services.area.return_value = ['nice']

        data = {'a': [0, 0], 'b': [10, 10]}
        data = PostArea(**data)
        result = await controller.area(data)

        services.area.assert_awaited_once_with(data)
        self.assertEqual(result, ['nice'])

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_coord(self, services):
        """ Calls `coord` service """
        services.coord.return_value = 'nice'

        data = {'x': 0, 'y': 10, 'c': 'x'}
        data = PostCoord(**data)
        result = await controller.coord(data)

        services.coord.assert_awaited_once_with(data)
        self.assertEqual(result, 'nice')

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_ws(self, services):
        """ Calls `subscribe` service """
        services.subscribe.side_effect = [None, None, Exception]

        ws = AsyncMock()
        with self.assertRaises(Exception):
            await controller.ws(ws)

        ws.connect.assert_awaited_once_with()
        services.subscribe.assert_awaited_with(ws)
        self.assertEqual(3, services.subscribe.call_count)
