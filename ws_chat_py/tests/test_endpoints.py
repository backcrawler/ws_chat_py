import json

from fastapi.testclient import TestClient

from ws_chat_py.server import app

client_1 = TestClient(app)
client_2 = TestClient(app)


def test_main_page():
    response = client_1.get('/')
    assert response.status_code == 200


def test_chat_start():
    init_response_1 = client_1.post('/init', data=json.dumps({'name': 'Anon'}))
    assert init_response_1.status_code == 200
    assert init_response_1.cookies.get('chat_auth_token')

    init_response_2 = client_2.post('/init', data=json.dumps({'name': 'Anon'}))
    assert init_response_2.status_code == 200
    assert init_response_2.cookies.get('chat_auth_token')

    start_response_1 = client_1.get('/start_chat')
    start_response_2 = client_2.get('/start_chat')
    assert start_response_1.status_code == 200
    assert start_response_2.status_code == 200
    assert start_response_1.json().get('chat')
    assert start_response_2.json().get('chat')
