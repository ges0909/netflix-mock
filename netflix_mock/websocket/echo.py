from starlette.websockets import WebSocket, WebSocketDisconnect


async def echo(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            await ws.send_json(data=data)
    except WebSocketDisconnect:
        pass
