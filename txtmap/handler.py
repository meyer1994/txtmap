import json
import logging

from .router import Router
from .actions import Actions
from .database import Connections

logger = logging.getLogger('Handler')
logger.setLevel(logging.INFO)


class Handler(Router):
    def __init__(self, url):
        super(Handler, self).__init__()
        self.connections = Connections(url)
        self.actions = Actions(url)

    @staticmethod
    def key(event):
        return event['requestContext']['eventType'].lower()

    def connect(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Connecting: %s', _id)
        self.connections.add(_id)
        logger.info('Connected: %s', _id)
        return {}

    def disconnect(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Disconnecting: %s', _id)
        self.connections.remove(_id)
        logger.info('Disconnected: %s', _id)
        return {}

    def message(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Start: %s', _id)
        body = event['body']
        event['body'] = json.loads(body)
        self.actions(event)
        logger.info('End: %s', _id)
        return {}
