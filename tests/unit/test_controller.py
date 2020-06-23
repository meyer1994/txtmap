from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock, MagicMock

from txtmap import controller
from txtmap.models import PostArea, PostCoord


class TestController(IsolatedAsyncioTestCase):

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_area(self, services):
        services.area.return_value = ['nice']

        data = {'a': [0, 0], 'b': [10, 10]}
        data = PostArea(**data)
        result = await controller.area(data)

        services.area.assert_awaited_once_with(data)
        self.assertEqual(result, ['nice'])

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_coord(self, services):
        services.coord.return_value = 'nice'

        data = {'x': 0, 'y': 10, 'c': 'x'}
        data = PostCoord(**data)
        result = await controller.coord(data)

        services.coord.assert_awaited_once_with(data)
        self.assertEqual(result, 'nice')

    @patch('txtmap.controller.services', new_callable=AsyncMock)
    async def test_ws(self, services):
        ws = MagicMock()
        await controller.ws(ws)
        services.subscribe.assert_awaited_once_with(ws)
