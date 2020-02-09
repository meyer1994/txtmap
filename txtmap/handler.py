import json
import logging

from .actions import Actions
from .database import Connections

logger = logging.getLogger('Handler')
logger.setLevel(logging.INFO)


class Handler(object):
    def __init__(self, url):
        super(Handler, self).__init__()
        self.connections = Connections(url)
        self.actions = Actions(url)

    def __call__(self, event, context):
        logger.info('Event:')
        logger.info(json.dumps(event))

        typ = event['requestContext']['eventType']
        logger.info('Type:')
        logger.info(typ)

        if typ == 'CONNECT':
            return self.connect(event, context)
        if typ == 'DISCONNECT':
            return self.disconnect(event, context)
        if typ == 'MESSAGE':
            return self.default(event, context)

    def connect(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Connecting:')
        logger.info(_id)

        self.connections.add(_id)
        return {}

    def disconnect(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Disconnecting:')
        logger.info(_id)

        self.connections.remove(_id)
        return {}

    def default(self, event, context):
        _id = event['requestContext']['connectionId']
        logger.info('Default:')
        logger.info(_id)

        body = event['body']
        event['body'] = json.loads(body)

        self.actions(event, context)
        return {}
