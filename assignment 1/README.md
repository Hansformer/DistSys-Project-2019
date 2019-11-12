# Assignment 1

Tasks:
- logging
- db = textfile: $chatroomname.txt only on server side (roni)
- client-server-client synchronization, send messages in the order server receives them


When a new client connects to server:
- Server sends list of chat rooms
- Client selects which room to join / create a new chat room and join it
- Send message history from chat room if it exists
- Synchronize new messages to all clients message by message

## server.py functionality (ATM)

Initially creates a dictionary with room names as keys taken from directory
*/chatrooms/*. The values for each key is a set (initially empty) which is updated
when a client connects to server and gives a room name (for example 'roomA.txt').
Sets are updated also when a client disconnects.

Steps in connecting to the server from a client:
1. When client connects server sends list of rooms to client.
2. Server waits for a response from client to choose a room (for example 'roomA.txt'
is a valid room).
3. Server waits for a messages from a client to send to every client in the same room.
4. Repeat 3.

Note that there is yet no implementation of writing the texts to rooms or sending the
history of the room to clients.
