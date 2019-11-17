import os
import config

from messagePersister import getPathForChatRoom, saveMessage, getMessageHistory


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

def getRooms():
    return rooms