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
async def init_handler(response: Response, chat_auth_token: Optional[str] = Cookie(...)):
    content = {'result': 'ok'}
    response = JSONResponse(content=content)
    response.set_cookie(key='chat_auth_token', value=uuid4().hex, httponly=False)
    return response


@root_router.get("/test")
async def init_handler(response: Response, request: Request, chat_auth_token: Optional[str] = Cookie(...)):
    print(f'COOKIE: {request.cookies}')
    return {'result': chat_auth_token}
