#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import websockets

connected = set()

async def handleIncMessage(socket):
    async for message in socket:
        for client in connected:
            await client.send(message)

async def handler(websocket, path):
    # Register.
    connected.add(websocket)
    task1 = asyncio.ensure_future(
        handleIncMessage(websocket)
    )

    try:
        done, pending = await asyncio.wait(
            [task1],
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()

    finally:
        connected.remove(websocket)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
