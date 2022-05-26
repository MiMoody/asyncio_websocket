import asyncio
import random
import websockets

 
async def server(websocket, path):
    try:
        while True:
            # Receive data from "the outside world"
            message = await websocket.recv()
            # Feed this data to the PUBLISH co-routine
            await websocket.send(f"Ok... {message} {random.randint(0, 1000)}")

    except websockets.exceptions.ConnectionClosed:
        print('Connection Closed!')
 
 
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(server, "localhost", 8200)
    loop.run_until_complete(start_server)
    loop.run_forever()

 