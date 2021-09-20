from typing import Optional, Dict

from fastapi import WebSocket, APIRouter, Cookie, status, Depends

from ws_chat_py.engines.person_engine import PersonEngine


ws_router = APIRouter()


@ws_router.websocket("/ws")
async def ws_chat_handler(websocket: WebSocket):
    await websocket.accept()
    authorized = check_chat_auth(websocket.cookies)
    if not authorized:
        await websocket.close()
        return
    new_person = PersonEngine.create_person(token=authorized, name='name')


    while True:
        try:
            txt = await websocket.receive_json()
            resp = {'msg': txt}
            await websocket.send_json(resp)
        except Exception as e:
            await websocket.close()
            break


def check_chat_auth(cookies: Dict[str, str]) -> Optional[str]:
    chat_auth_token = cookies.get('chat_auth_token')
    if not chat_auth_token:
        return None
    return chat_auth_token
