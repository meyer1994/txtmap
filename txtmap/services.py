from typing import Tuple, List

from txtmap.db import database


async def area(a: Tuple[int, int], b: Tuple[int, int]) -> List[dict]:
    ax, ay = a
    bx, by = b
    values = {'ax': ax, 'ay': ay, 'bx': bx, 'by': by}
    query = r'''
        SELECT * FROM coordinates
        WHERE box (point (:ax, :ay), point (:bx, :by)) @> point (x, y)
    '''
    return database.fetch_all(query=query, values=values)


async def coord(x: int, y: int) -> dict:
    pass


async def subscribe():
    pass


async def publish(data: dict):
    pass
