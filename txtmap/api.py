from fastapi import FastAPI
from broadcaster import Broadcast
from starlette.websockets import WebSocket

from txtmap.config import config

broadcast = Broadcast(config.BROADCASTER_URL)
app = FastAPI()


@app.on_event('startup')
async def startup():
    await broadcast.connect()


@app.on_event('shutdown')
async def shutdown():
    await broadcast.disconnect()


@app.websocket('/')
async def websocket(ws: WebSocket):
    await ws.accept()
    async with broadcast.subscribe(channel='map') as subscriber:
        async for event in subscriber:
            await ws.send_text(event.message)


@app.post('/')
async def post():
    await broadcast.publish(channel='map', message='nice')
