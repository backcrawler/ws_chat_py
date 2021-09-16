import uvicorn

from ws_chat_py.server import app
from ws_chat_py.configs import HOST, PORT


if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
