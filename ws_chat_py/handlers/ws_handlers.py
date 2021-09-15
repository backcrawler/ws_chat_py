from typing import Optional, Dict

from fastapi import WebSocket, APIRouter, Cookie, status, Depends


ws_router = APIRouter()


@ws_router.websocket("/ws")
async def ws_chat_handler(websocket: WebSocket):
    await websocket.accept()
    authorized = check_chat_auth(websocket.cookies)
    if not authorized:
        print('User unathorized')
        await websocket.close()
        return

    while True:
        try:
            txt = await websocket.receive_json()
            resp = {'msg': txt}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            await websocket.close()
            break


def check_chat_auth(cookies: Dict[str, str]) -> bool:
    print(f'COOKIES: {cookies}')
    chat_auth_token = cookies.get('chat_auth_token')
    if not chat_auth_token:
        return False
    return True
