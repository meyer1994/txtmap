from fastapi import FastAPI
from broadcaster import Broadcast
from starlette.websockets import WebSocket

from txtmap.config import config
from txtmap.models import PostModel
from txtmap.db import database, Coordinate


broadcast = Broadcast(config.DATABASE_URL)
app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()
    await broadcast.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    await broadcast.disconnect()


@app.websocket('/')
async def websocket(ws: WebSocket):
    await ws.accept()
    async with broadcast.subscribe(channel='map') as subscriber:
        async for event in subscriber:
            await ws.send_text(event.message)


@app.post('/')
async def post(data: PostModel):
    await Coordinate.objects.create(**data.dict())
    await broadcast.publish(channel='map', message=data.json())
    return data


@app.get('/area')
async def get(ax: int, ay: int, bx: int, by: int):
    values = {'ax': ax, 'ay': ay, 'bx': bx, 'by': by}
    query = r'''
        SELECT * FROM coordinates
        WHERE box (point (:ax, :ay), point (:bx, :by)) @> point (x, y)
    '''
    return await database.fetch_all(query=query, values=values)
