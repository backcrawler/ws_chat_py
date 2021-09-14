from fastapi import WebSocket, APIRouter


ws_router = APIRouter()


@ws_router.websocket("/ws")
async def ws_chat_handler(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            await websocket.receive_text()
            resp = {'msg': f'Debug: {i}'}
            i += 1
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
