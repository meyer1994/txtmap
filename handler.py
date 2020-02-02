import os
import json
import logging

import boto3

from txtmap.database import TextMap

DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def respond(event, data):
    domain = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    url = f'https://{domain}/{stage}'

    gatewayapi = boto3.client('apigatewaymanagementapi', endpoint_url=url)

    connection = event['requestContext']['connectionId']
    data = json.dumps(data)

    gatewayapi.post_to_connection(ConnectionId=connection, Data=data)

    return {'statusCode': 200, 'body': data}


def connect(event, context):
    connection = event['requestContext']['connectionId']
    logger.info('CONNECT: %s', connection)
    return {'statusCode': 200, 'id': connection}


def disconnect(event, context):
    connection = event['requestContext']['connectionId']
    logger.info('CONNECT: %s', connection)
    return {'statusCode': 200, 'id': connection}


def default(event, context):
    body = event['body']
    body = json.loads(body)

    action = body['action']

    x, y = body['x'], body['y']
    x, y = int(x), int(y)

    db = TextMap(URL)

    if action == 'GET':
        data = db.get(x, y)
        data = {'x': data.x, 'y': data.y, 'char': data.char}
        return respond(event, data)

    if action == 'SET':
        char = body['char']
        data = db.set(x, y, char)
        data = {'x': data.x, 'y': data.y, 'char': data.char}
        return respond(event, data)

    if action == 'AREA':
        width, heigth = body['width'], body['heigth']
        width, heigth = int(width), int(heigth)
        data = db.area(x, y, width, heigth)
        data = [{'x': d.x, 'y': d.y, 'char': d.char} for d in data]
        return respond(event, data)


def handler(event, context):
    logger.info(json.dumps(event))

    event_type = event['requestContext']['eventType']

    if event_type == 'CONNECT':
        return connect(event, context)
    if event_type == 'DISCONNECT':
        return disconnect(event, context)
    if event_type == 'MESSAGE':
        return default(event, context)

    return {'statusCode': 500}
