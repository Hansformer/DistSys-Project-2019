#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import threading

async def getNewMessages(socket):

    while(True):
        message = await socket.recv()
        print(message)
        if(message == "Goodbye Client"):
            break
    
    return

async def sendNewMessages(socket):

    while(True):
        message = input("Next Message: ")
        if message == "stop":
            break                
        await socket.send(message)
    
    return

async def chat():

    try: 
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            
            readerThread = threading.Thread(target=getNewMessages,args=[websocket])
            senderThread = threading.Thread(target=sendNewMessages,args=[websocket])
            
            senderThread.join()
            readerThread.join()
            
    except websockets.exceptions.ConnectionClosedError: 
        # TODO: log this 
        print("Unfortenataly we lost connection to Server") 


asyncio.get_event_loop().run_until_complete(chat())