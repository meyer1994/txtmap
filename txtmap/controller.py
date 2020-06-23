from fastapi import APIRouter
from starlette.websockets import WebSocket

from txtmap.models import PostArea, PostCoord

router = APIRouter()


@router.websocket('/ws')
async def ws(ws: WebSocket):
    pass


@router.post('/area')
async def area(data: PostArea):
    pass


@router.post('/coord')
async def coord(data: PostCoord):
    pass
