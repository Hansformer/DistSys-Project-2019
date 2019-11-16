#!/usr/bin/env python

# WS client example

import asyncio
import datetime
import websockets
from aioconsole import ainput
import config

from logger import Logger

logger = Logger("./logs/client-{}.txt".format(datetime.datetime.now()), config.LOGLEVEL)

async def getNewMessages(socket):

    async for message in socket:
        logger.logDebug("New message: {}".format(message))
        # Chat history is received as bytes
        if type(message) is bytes:
            print(message.decode("utf-8"))
        else:
            print(message)

            if(message == "Goodbye Client"):
                break



async def sendNewMessages(socket):

    while(True):
        # read message from CLI
        message = await ainput("Next Message: ")
        if message == "stop":
            logger.logMsg("Stopping client.")
            break
        await socket.send(message)
        logger.logMsg("Sent message: {}".format(message))
        # tiny sleep so the other corotines can do their thing
        await asyncio.sleep(0.01)

async def chat():

    try:
        uri = "ws://localhost:8765"
        # connect to server
        async with websockets.connect(uri) as websocket:
            logger.logMsg("Connected to server: {}".format(uri))
            # getting chatrooms from server
            s = await websocket.recv()
            logger.logMsg("Received message from server: {}".format(s))
            
            chatrooms = s[s.find("[") +1 :s.find("]")].split(", ")
            
            # print chatrooms linewise
            for room in chatrooms:
                print(room)
            
            answer = input("Which of the above chatrooms do you want to enter? ")
            
            if "'" + answer + "'" in chatrooms:
                await websocket.send(answer)
            else:
                # break if there is no such chatroom
                print(answer)
                print("There is no Chatroom called like that")
                return

            # corotine for recieving messages from server
            task1 = asyncio.create_task(
                getNewMessages(websocket)
            )
            # corotine for recieving messages from server
            task2 = asyncio.create_task(
                sendNewMessages(websocket)
            )
            # start corotines
            done, pending = await asyncio.wait(
                [task1, task2],
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()

    except websockets.exceptions.ConnectionClosedError:
        # TODO: log this
        logger.logError("Connection to server lost.")
        print("Unfortenataly we lost connection to Server")


asyncio.get_event_loop().run_until_complete(chat())
