#!/usr/bin/env python

# WS client example

import asyncio
import datetime
import random
import sys
import websockets
from aioconsole import ainput
import config

from logger import Logger

logger = Logger("./logs/client-{}.txt".format(datetime.datetime.now()), config.LOGLEVEL)

async def printIterator(message):
	length = len(message)
	chunksize = 1024
	for i in range(0, length, chunksize):
		print(message[i:i + chunksize])

async def receiveMessage(socket):
    async for message in socket:

        # Chat history is received as bytes
        if type(message) is bytes:
            logtask = loop.create_task(logger.logMsg("Chat log received."))
            await asyncio.wait([logtask])
            if len(message) > 1024:
                task = loop.create_task(printIterator(message.decode("utf-8")))
                await asyncio.wait([task])
            else:
                print(message.decode("utf-8"))
        else:
            logtask = loop.create_task(logger.logMsg("New message received."))
            await asyncio.wait([logtask])
            if len(message) > 1024:
                task = loop.create_task(printIterator(message))
                await asyncio.wait([task])
            else:
                print(message)

            if(message == "Goodbye Client"):
                break



async def sendMessage(socket):

    while(True):
        # read message from CLI
        message = await ainput("Message to send: ")

        if message == "stop":
            await logger.logMsg("Stopping client.")
            break

        await socket.send(message)

        await logger.logMsg("Sent message: {}".format(message))

        # Run benchmarking with file
        if config.BENCHMARK:
            filep = open("./chatrooms/1MB_crash_test.txt", "r")
            data = filep.read()
            filep.close()
            await logger.logMsg("Starting filesend")
            for i in range(0,24):
                await socket.send(data)
            await logger.logMsg("Ending filesend")

        # tiny sleep so the other corotines can do their thing
        await asyncio.sleep(0.01)

async def chat():

    try:
        uri = "ws://localhost:8765"
        # connect to server
        async with websockets.connect(uri) as websocket:
            await logger.logMsg("Connected to server: {}".format(uri))
            # getting chatrooms from server
            chatRoomsResponse = await websocket.recv()
            await logger.logMsg("Received message from server: {}".format(chatRoomsResponse))
            
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
        await logger.logError("Connection to server lost.")
        print("Unfortenataly we lost connection to Server")

loop = asyncio.get_event_loop()
loop.run_until_complete(chat())
loop.close()
