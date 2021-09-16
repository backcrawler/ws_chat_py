from uuid import uuid4
from typing import Optional

from fastapi import Request, APIRouter, Response, Cookie, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from ..configs import STATIC_DIR


root_router = APIRouter()
templates = Jinja2Templates(directory=f"{STATIC_DIR}/templates")


@root_router.get("/", response_class=HTMLResponse)
async def root_handler(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@root_router.get("/init")
async def init_handler():
    content = {'result': 'ok1'}
    response = JSONResponse(content=content)
    response.headers["X-Cat-Dog"] = "alone in the world"
    response.set_cookie(key='chat_auth_token', value=uuid4().hex, httponly=False)
    return response


@root_router.get("/test")
async def test_handler(response: Response, request: Request):
    print(f'COOKIES: {request.cookies}')
    print(f'HEADERS: {request.headers}')
    return {'result': 'ok'}
