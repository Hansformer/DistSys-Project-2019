
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
has_room = {}

def getCurrentRoom(websocket):
    for room in d:
        if websocket in d[room]:
            return room
    return ''

async def handleMessage(socket):
    while True:
        msg = await socket.recv()
        if socket in has_room:
            if has_room[socket] == True:
                current_room = getCurrentRoom(socket)
                for client in d[current_room]:
                        await client.send(msg)
                        print(str(socket), 'sent message: "', msg, '"')

            else:
                if msg in d.keys():
                    d[msg].add(socket)
                    has_room[socket] = True
                    print("Client", str(socket), "connected to room", msg)


async def handler(websocket, path):

    await websocket.send(str(d.keys()))
    has_room[websocket] = False

    task = asyncio.ensure_future(
        handleMessage(websocket)
    )

    try:
        current_room = getCurrentRoom(websocket)
        done, pending = await asyncio.wait(
                [task]
        )

        for task in pending:
            task.cancel()

    finally:
        current_room = getCurrentRoom(websocket)
        if current_room != '':
            d[current_room].remove(websocket)
            del has_room[websocket]
        print(d)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
