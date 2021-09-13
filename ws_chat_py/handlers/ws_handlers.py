from fastapi import WebSocket, APIRouter


ws_router = APIRouter()


@ws_router.get("/ws")
async def ws_chat_handler(websocket: WebSocket):
    print('Accepting client connection...')  # todo: remove
    await websocket.accept()
    i = 0  # todo: revise
    while True:
        try:
            # Wait for any message from the client
            await websocket.receive_text()
            # Send message to the client
            resp = {'msg': f'Debug: {i}'}
            i += 1
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('End connection..')
