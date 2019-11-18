import asyncio
import websockets
import os
import config

from logger import Logger
from messagePersister import getPathForChatRoom, saveMessage, getMessageHistory
from roomHelper import getCurrentRoom, getRooms

logger = Logger(config.SERVERLOG, config.LOGLEVEL)

async def handleMessage(socket):
    await logger.logDebug("handleMessage(): Entering")

    while True:
        try:
            msg = await socket.recv()

            await logger.logDebug("Server received message")

            current_room = getCurrentRoom(socket)

            rooms = getRooms();

            if current_room != '':
                for client in rooms[current_room]:
                        await client.send(msg)
                        await logger.logMsg("{} sent message".format(str(socket)))
                        saveMessage(current_room, msg);

            else:
                if msg in rooms.keys():
                    rooms[msg].add(socket)
                    await logger.logMsg("Client {} connected connected to room: {}".format(str(socket), msg))
                    messageHistory = getMessageHistory(msg);
                    await socket.send(messageHistory)

        except websockets.ConnectionClosed:
            pass

    await logger.logDebug("handleMessage(): Exiting")

async def handler(websocket, path):
    await logger.logDebug("handler(): Entering")

    rooms = getRooms();

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
            await logger.logMsg("Client {} has left {}.".format(str(websocket), current_room))

start_server = websockets.serve(handler, "localhost", 8765)
logger.logMsg("Server started, listening on 'localhost:8765'")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
