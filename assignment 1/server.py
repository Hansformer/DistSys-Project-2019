
import asyncio
import json
import websockets
import os
import config

def createDictforRooms():
    rooms = [f for f in os.listdir(config.CHAT) if os.path.isfile(os.path.join(config.CHAT, f))]
    d = dict()
    for room in rooms:
        d[room] = set()
    return d

d = createDictforRooms()

def getCurrentRoom(websocket):
    for room in d:
        if websocket in d[room]:
            return room
    return ''

async def handleIncMessage(socket):
    current_room = getCurrentRoom(socket)
    async for message in socket:
        for client in d[current_room]:
            await client.send(message)

async def handleInit(socket):
    async for roomname in socket:
        if roomname in d:
            d[roomname].add(socket)
            print(d)

async def handler(websocket, path):

    init_task = asyncio.ensure_future(
        handleInit(websocket)
    )


    # task1 = asyncio.ensure_future(
    #     handleIncMessage(websocket)
    # )

    try:

        done, pending = await asyncio.wait(
            [init_task],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

    finally:
        current_room = getCurrentRoom(websocket)
        if current_room != '':
            d[current_room].remove(websocket)
        print(d)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
