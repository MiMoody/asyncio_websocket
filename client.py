import sys
import asyncio
from websockets import connect
from parser_params import set_params_url


class EchoWebsocket:
    def __await__(self,):
        return self._async_init().__await__()

    async def _async_init(self):
        url = set_params_url("ws://localhost:8200", params={"model":"big_en", "sample_rate":8000})
        self._conn = connect(url)
        self.websocket = await self._conn.__aenter__()
        return self

    async def close(self):
        await self._conn.__aexit__(*sys.exc_info())

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


async def main():
    echo = await EchoWebsocket()
    try:
        while True:
            await echo.send("Hello!")
            print(await echo.receive())  # "Hello!"
            await asyncio.sleep(1)
    finally:
        await echo.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())