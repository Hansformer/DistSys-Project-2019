#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def getNewMessages(socket):

    async for message in socket:
        print(message)
        if(message == "Goodbye Client"):
            break
        


async def sendNewMessages(socket):

    while(True):
        # read message from CLI
        message = input("Next Message: ")
        if message == "stop":
            break                
        await socket.send(message)
        # tiny sleep so the other corotines can do their thing
        await asyncio.sleep(0.01)

async def chat():

    try: 
        uri = "ws://localhost:8765"
        # connect to server
        async with websockets.connect(uri) as websocket:
            # corotine for recieving messages from server
            task1 = asyncio.ensure_future(
                getNewMessages(websocket)
            )
            # corotine for recieving messages from server
            task2 = asyncio.ensure_future(
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
        print("Unfortenataly we lost connection to Server") 


asyncio.get_event_loop().run_until_complete(chat())