from typing import List

from broadcaster import Broadcast
from starlette.websockets import WebSocket

from txtmap.config import config
from txtmap.db import database, Coordinate
from txtmap.models import PostArea, PostCoord


broadcast = Broadcast(config.DATABASE_URL)


async def area(box: PostArea) -> List[dict]:
    ax, ay = box.a
    bx, by = box.b
    values = {'ax': ax, 'ay': ay, 'bx': bx, 'by': by}
    query = r'''
        SELECT * FROM coordinates
        WHERE box (point (:ax, :ay), point (:bx, :by)) @> point (x, y)
    '''
    return database.fetch_all(query=query, values=values)


async def coord(coord: PostCoord) -> dict:
    await Coordinate.objects.create(**coord.dict())
    return coord.dict()


async def subscribe(ws: WebSocket):
    async with broadcast.subscribe(channel='map') as subscriber:
        async for event in subscriber:
            await ws.send_text(event.message)


async def publish(data: dict):
    pass
