def test_echo(client):
    with client.websocket_connect("/ws/echo") as ws:
        data = dict(msg="Hello WebSocket")
        ws.send_json(data=data)
        data_ = ws.receive_json()
        assert data_ == data
