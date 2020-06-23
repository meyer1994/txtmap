from fastapi import APIRouter
from starlette.websockets import WebSocket

from txtmap import services
from txtmap.models import PostArea, PostCoord

router = APIRouter()


@router.websocket('/ws')
async def ws(ws: WebSocket):
    raise NotImplementedError()


@router.post('/area')
async def area(data: PostArea):
    return await services.area(data)


@router.post('/coord')
async def coord(data: PostCoord):
    return await services.coord(data)
