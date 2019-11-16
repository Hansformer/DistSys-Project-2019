import os
import config

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