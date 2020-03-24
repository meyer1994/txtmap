import json
import logging

import boto3

from .router import Router
from .database import Connections, TextMap

logger = logging.getLogger('Actions')
logger.setLevel(logging.INFO)


class Actions(Router):
    def __init__(self, url):
        super(Actions, self).__init__()
        self.map = TextMap(url)
        self.connections = Connections(url)

    @staticmethod
    def key(event):
        return event['body']['action'].lower()

    def get(self, event):
        body = event['body']
        x, y = body['x'], body['y']
        x, y = int(x), int(y)

        logger.info('Get:')
        logger.info('(%s, %s)', x, y)

        data = self.map.get(x, y)
        _id = event['requestContext']['connectionId']
        return self.send(event, [data], [_id])

    def set(self, event):
        body = event['body']
        x, y = body['x'], body['y']
        x, y = int(x), int(y)
        char = body['char']

        logger.info('Set:')
        logger.info('(%s, %s) => %s', x, y, char)

        data = self.map.set(x, y, char)
        ids = self.connections.all()
        return self.send(event, [data], ids)

    def area(self, event):
        body = event['body']
        x, y = body['x'], body['y']
        x, y = int(x), int(y)
        width, heigth = body['width'], body['heigth']
        width, heigth = int(width), int(heigth)

        logger.info('Area:')
        logger.info('(%s, %s), (%s, %s)', x, y, width, heigth)

        data = self.map.area(x, y, width, heigth)
        _id = event['requestContext']['connectionId']
        return self.send(event, data, [_id])

    def send(self, event, data, ids):
        # Build URL
        domain = event['requestContext']['domainName']
        stage = event['requestContext']['stage']
        url = f'https://{domain}/{stage}'

        gatewayapi = boto3.client('apigatewaymanagementapi', endpoint_url=url)

        data = json.dumps(data)
        for _id in ids:
            gatewayapi.post_to_connection(ConnectionId=_id, Data=data)

        return {}
