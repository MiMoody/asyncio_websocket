import websockets
from websockets import WebSocketServerProtocol
import logging

logging.basicConfig(level=logging.INFO)

class BaseServer:
    clients = set()

    async def register(self, ws:WebSocketServerProtocol)-> None:
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects!")
    
    async def unregister(self, ws:WebSocketServerProtocol)-> None:
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects!")

    async def send(self, ws:WebSocketServerProtocol, message):
        if ws in self.clients:
            await ws.send(message)
    
    async def ws_handler(self, ws:WebSocketServerProtocol)-> None:
        await self.register(ws)
        try:
            await self.distribute(ws)
        finally:
            await self.unregister(ws)

    async def distribute(self, ws:WebSocketServerProtocol)-> None:
        try:
            async for message in ws:
                await self.send(ws, str(message))
        except websockets.ConnectionClosed as e:
            print(f'Terminated', e)

 