import logging
from unittest import TestCase

from txtmap.router import Router


class SimpleRouter(Router):
    @staticmethod
    def key(event):
        keys = list(event.keys())
        return keys[0]

    def nice(self, event):
        return event['nice'] * 2


class TestItems(TestCase):
    def test_route(self):
        """ Routes correctly based on key """
        router = SimpleRouter()
        event = {'nice': 5}
        result = router(event)
        self.assertEqual(result, 10)

    def test_logs(self):
        """ Assert the router logs """
        with self.assertLogs(level=logging.INFO):
            self.test_route()
