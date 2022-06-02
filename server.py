import uuid
import websockets
from websockets import WebSocketServerProtocol
import logging
from parser_params import get_params_url

logging.basicConfig(level=logging.INFO)

class BaseClient:
    def __init__(self, 
                ws:WebSocketServerProtocol,
                ):
        self.__id = str(uuid.uuid4())
        self.__ws = ws

    @property
    def ws(self):
        return self.__ws
    
    def __str__(self):
        return f"Client with id: {self.__id}"

class BaseServer():
    clients = set()

    async def register(self, ws:WebSocketServerProtocol, url:str):
        url = f"ws://{ws._host}:{ws._port}{url}"
        params = get_params_url(url)
        client = BaseClient(ws)
        self.clients.add(client)
        logging.info(f"{client} connects!")
        return client
    
    async def unregister(self, client)-> None:
        self.clients.remove(client)
        logging.info(f"{client} disconnects!")

    async def send(self, client, message):
        if client in self.clients:
            await client.ws.send(message)
    
    async def ws_handler(self, ws:WebSocketServerProtocol, url:str)-> None:
        client = await self.register(ws, url)
        try:
            await self.distribute(client)
        finally:
            await self.unregister(client)

    async def distribute(self, client)-> None:
        try:
            async for message in client.ws:
                await self.send(client, str(message))
        except websockets.ConnectionClosed as e:
            print(f'Terminated', e)

 