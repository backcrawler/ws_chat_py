import asyncio
from uuid import uuid4
from typing import Optional

from fastapi import Request, APIRouter, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from ..configs import STATIC_DIR
from ..engines import PersonEngine
from ..managers import chat_manager, delta_manager
from ..schemas.request_schemas import IncomingMessage, ActionCommand, InitRequest
from ..schemas.response_schemas import SimpleResponse, DeltaResponse


root_router = APIRouter()
templates = Jinja2Templates(directory=f'{STATIC_DIR}/templates')


@root_router.get("/", response_class=HTMLResponse)
async def root_handler(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@root_router.post('/init', response_model=SimpleResponse)
async def init_handler(init_data: InitRequest, request: Request):
    cookie = request.cookies.get('chat_auth_token')
    response = JSONResponse(content={'result': 'ok'})
    if cookie:
        return response

    new_cookie = uuid4().hex
    PersonEngine.create_person(new_cookie, init_data.name)
    response.set_cookie(key='chat_auth_token', value=new_cookie, httponly=False)  # todo: httponly
    return response


@root_router.get('/start_chat', response_model=SimpleResponse)
async def start_chat_handler(request: Request):
    cookie = request.cookies.get('chat_auth_token')
    if not cookie:
        raise HTTPException(status_code=401, detail='unauthorized')

    await PersonEngine.set_new_chat_for_person(cookie)
    return ...


@root_router.get('/delta', response_model=DeltaResponse)
async def delta_handler(ch_id: str, request: Request):
    authorized = check_auth_for_chat(ch_id, request.cookies.get('chat_auth_token'))
    if not authorized:
        raise HTTPException(status_code=401, detail='unauthorized')

    deltas = await delta_manager.get_deltas_for_chat(ch_id)
    if not deltas:
        return JSONResponse({'result': 'reinit-required'})

    return JSONResponse(content={'result': deltas})


@root_router.post('/action', response_model=SimpleResponse)
async def action_handler(action_cmd: ActionCommand, request: Request):
    authorized = check_auth_for_chat(action_cmd.ch_id, request.cookies.get('chat_auth_token'))
    if not authorized:
        raise HTTPException(status_code=401, detail='unauthorized')

    chat = chat_manager.get_chat_by_id(action_cmd.ch_id)
    chat.engine.process_action()
    return JSONResponse(content={'result': 'ok'})


@root_router.post('/message')
async def message_handler(msg: IncomingMessage, request: Request):
    authorized = check_auth_for_chat(msg.ch_id, request.cookies.get('chat_auth_token'))
    if not authorized:
        raise HTTPException(status_code=401, detail='unauthorized')

    chat = chat_manager.get_chat_by_id(msg.ch_id)
    chat.engine.create_basic_message(msg.text, msg.ch_id, request.cookies.get('chat_auth_token'))
    return JSONResponse({'result': 'ok'})


def check_auth_for_chat(ch_id: str, token: Optional[str]) -> bool:  # todo: Dependable
    if not token:
        return False

    current_chat = chat_manager.get_chat_by_id(ch_id)
    if not current_chat:
        return False

    return current_chat.engine.check_auth_for_members(token)
