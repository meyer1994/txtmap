import inspect
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger('Router')
logger.setLevel(logging.INFO)


class Router(ABC):
    def __init__(self):
        super(Router, self).__init__()
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        self.methods = {k: v for k, v in methods if not k.startswith('_')}

    def __call__(self, event, *args, **kwargs):
        key = self.key(event)
        logger.info('Route: %s', key)
        function = self.methods[key]
        return function(event, *args, **kwargs)

    @staticmethod
    @abstractmethod
    def key(event):
        pass
