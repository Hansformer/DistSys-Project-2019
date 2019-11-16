import asyncio
import json
import websockets
import os
import config

from logger import Logger

logger = Logger(config.SERVERLOG, config.LOGLEVEL)

def getPathForChatRoom(room):
    return os.path.join(config.CHATROOMS_DIR, room)

def saveMessage(room, msg):
    # TODO: Reuse file pointers
    roomFile = open(getPathForChatRoom(room), "a+")
    roomFile.write(msg + "\r\n");
    roomFile.flush();
    roomFile.close();

def getMessageHistory(room):
    # TODO: Ensure that client can't open any other files that the ones in the config.CHAT dir (by using ../ in file path)
    roomFile = open(getPathForChatRoom(room), "rb")
    messages = roomFile.read()
    roomFile.close()
    return messages

def createDictforRooms():
    rooms = [f for f in os.listdir(config.CHATROOMS_DIR) if os.path.isfile(getPathForChatRoom(f))]
    d = dict()
    for room in rooms:
        d[room] = set()
    return d

rooms = createDictforRooms()

def getCurrentRoom(websocket):
    for room in rooms:
        if websocket in rooms[room]:
            return room
    return ''

async def handleMessage(socket):
    logger.logDebug("handleMessage(): Entering")

    while True:
        try:
            msg = await socket.recv()

            logger.logDebug("Server received message: \"{}\"".format(msg))

            current_room = getCurrentRoom(socket)

            if current_room != '':
                for client in rooms[current_room]:
                        await client.send(msg)
                        logger.logMsg("{} sent message: \"{}\"".format(str(socket), msg))
                        saveMessage(current_room, msg);

            else:
                if msg in rooms.keys():
                    rooms[msg].add(socket)
                    logger.logMsg("Client {} connected connected to room: {}".format(str(socket), msg))
                    messageHistory = getMessageHistory(msg);
                    await socket.send(messageHistory)

        except websockets.ConnectionClosed:
            pass

    logger.logDebug("handleMessage(): Exiting")

async def handler(websocket, path):
    logger.logDebug("handler(): Entering")

    await websocket.send(str(rooms.keys()))

    task = asyncio.ensure_future(
        handleMessage(websocket)
    )

    try:
        _, pending = await asyncio.wait(
                [task]
        )

        for task in pending:
            task.cancel()
            
    finally:
        current_room = getCurrentRoom(websocket)

        if current_room != '':
            rooms[current_room].remove(websocket)
            logger.logMsg("Client {} has left {}.".format(str(websocket), current_room))

start_server = websockets.serve(handler, "localhost", 8765)
logger.logMsg("Server started, listening on 'localhost:8765'")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
