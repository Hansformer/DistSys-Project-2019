#!/usr/bin/env python

# WS client example

import asyncio
import datetime
import websockets
from aioconsole import ainput
import config

from logger import Logger

logger = Logger("./logs/client-{}.txt".format(datetime.datetime.now()), config.LOGLEVEL)

async def receiveMessage(socket):
    async for message in socket:
        logger.logDebug("New message: {}".format(message))

        # Chat history is received as bytes
        if type(message) is bytes:
            print(message.decode("utf-8"))
        else:
            print(message)

            if(message == "Goodbye Client"):
                break



async def sendMessage(socket):

    while(True):
        # read message from CLI
        message = await ainput("Message to send: ")

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
            chatRoomsResponse = await websocket.recv()
            logger.logMsg("Received message from server: {}".format(chatRoomsResponse))
            
            chatrooms = chatRoomsResponse[chatRoomsResponse.find("[") +1 :chatRoomsResponse.find("]")].split(", ")
            
            # print chatrooms linewise
            for room in chatrooms:
                print(room)
            
            chatRoomToJoin = input("Which of the above chatrooms do you want to join? ")
            
            if "'" + chatRoomToJoin + "'" in chatrooms:
                await websocket.send(chatRoomToJoin)
            else:
                # break if there is no such chatroom
                print(chatRoomToJoin)
                print("There is no Chatroom called like that")
                return

            # corotine for recieving messages from server
            receiveMessageTask = asyncio.create_task(
                receiveMessage(websocket)
            )
            # corotine for sending messages to server
            sendMessageTask = asyncio.create_task(
                sendMessage(websocket)
            )
            # start corotines
            _, pending = await asyncio.wait(
                [receiveMessageTask, sendMessageTask],
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()

    except websockets.exceptions.ConnectionClosedError:
        logger.logError("Connection to server lost.")
        print("Unfortenataly we lost connection to Server")


asyncio.get_event_loop().run_until_complete(chat())
