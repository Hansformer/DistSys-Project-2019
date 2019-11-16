import os
import config

filePointers = {}

def getPathForChatRoom(room):
    return os.path.join(config.CHATROOMS_DIR, room)

def saveMessage(room, msg):
    if room not in filePointers:
        filePointers[room] = open(getPathForChatRoom(room), "a+")

    roomFile = filePointers[room]
    roomFile.write(msg + "\r\n");
    roomFile.flush();

# TODO: Close files on exit
def closeFiles():
    for file in filePointers:
        file.close();

def getMessageHistory(room):
    # TODO: Ensure that client can't open any other files that the ones in the config.CHAT dir (by using ../ in file path)
    roomFile = open(getPathForChatRoom(room), "rb")
    messages = roomFile.read()
    roomFile.close()
    return messages