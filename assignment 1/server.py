import asyncio
import json
import websockets
import os
import config

from logger import Logger

logger = Logger(config.SERVERLOG, config.LOGLEVEL)


def saveMessage(room, msg):
    # TODO: Reuse file pointers
    f = open(config.CHAT + room, "a+")
    f.write(msg + "\r\n");
    f.flush();
    f.close();

def getMessageHistory(room):
    # TODO: Ensure that client can't open any other files that the ones in the config.CHAT dir (by using ../ in file path)
    f = open(config.CHAT + room, "rb")
    return f.read()

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
    logger.logDebug("handleMessage(): Entering")
    while True:
        try:
            msg = await socket.recv()
            logger.logDebug("Server received message: \"{}\"".format(msg))
            if socket in has_room:
                if has_room[socket] == True:
                    current_room = getCurrentRoom(socket)
                    for client in d[current_room]:
                            await client.send(msg)
                            print(str(socket), 'sent message: "', msg, '"')
                            saveMessage(current_room, msg);

                else:
                    if msg in d.keys():
                        d[msg].add(socket)
                        has_room[socket] = True
                        logger.logMsg("Client {} connected connected to room: {}".format(str(socket), msg))
                        messageHistory = getMessageHistory(msg);
                        await socket.send(messageHistory)
        except websockets.ConnectionClosed:
            pass
    logger.logDebug("handleMessage(): Exiting")

async def handler(websocket, path):

    logger.logDebug("handler(): Entering")
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
            logger.logMsg("Client {} has left {}.".format(str(websocket), current_room))

start_server = websockets.serve(handler, "localhost", 8765)
logger.logMsg("Server started, listening on 'localhost:8765'")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
