from starlette.websockets import WebSocket


async def echo(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        await ws.send_json(data=data)
