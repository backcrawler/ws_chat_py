import asyncio
from uuid import uuid4
from typing import Optional

from fastapi import Request, APIRouter, Response, Cookie, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from ..configs import STATIC_DIR
from ..managers.chat_manager import chat_manager
from ..managers.delta_manager import delta_manager


root_router = APIRouter()
templates = Jinja2Templates(directory=f"{STATIC_DIR}/templates")


@root_router.get("/", response_class=HTMLResponse)
async def root_handler(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@root_router.get('/init')
async def init_handler():
    content = {'result': 'ok'}
    response = JSONResponse(content=content)
    response.set_cookie(key='chat_auth_token', value=uuid4().hex, httponly=False)
    return response


@root_router.get('/test')
async def test_handler(response: Response, request: Request):
    print(f'TEST COOKIES: {request.cookies}')
    print(f'TEST HEADERS: {request.headers}')
    i = 0
    while True:
        print(f'I: {i}')
        if i >= 10:
            break
        await asyncio.sleep(1)
        i += 1
    return {'result': f'{i}'}


@root_router.get('/delta')
async def delta_handler(ch_id: str, request: Request):
    authorized = check_auth_for_chat(ch_id, request.cookies.get('chat_auth_token'))
    # if not authorized:
    #     return

    deltas = await delta_manager.get_deltas_for_chat(ch_id)
    if not deltas:
        return JSONResponse({'result': 'reinit-required'})

    return JSONResponse(content={'result': deltas})


def check_auth_for_chat(ch_id: str, token: Optional[str]) -> bool:
    if not token:
        return False

    current_chat = chat_manager.get_chat_by_id(ch_id)
    if not current_chat:
        return False

    return current_chat.engine.check_auth_for_members(token)
