from typing import Tuple, List

from txtmap.db import database, Coordinate
from txtmap.models import PostArea, PostCoord


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


async def subscribe():
    pass


async def publish(data: dict):
    pass
