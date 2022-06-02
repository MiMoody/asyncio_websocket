import asyncio
import websockets
from server import  BaseServer


if __name__ == '__main__':
    # Boiler-plate for the websocket server, running on localhost, port 8765
    server = BaseServer()
    ws_server = websockets.serve(server.ws_handler, 'localhost', 8200)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ws_server)
    loop.run_forever()