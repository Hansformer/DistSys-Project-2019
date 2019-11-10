This will be the central repo for all Distributed Systems assignments

Tasks: 
- logging
- db = textfile: $chatroomname.txt only on server side (ronni)
- client-server-client synchronization, send messages in the order server receives them 


When a new client connects to server: 
- Server sends list of chat rooms
- Client selects which room to join / create a new chat room and join it
- Send message history from chat room if it exists
- Synchronize new messages to all clients message by message

# Development
`cd [assignment_name]`

Install virtualenv to `./venv/`:

`python3 -m venv ./venv`

Activate virtualenv:

`source ./venv/bin/activate`


Install dependencies:
`pip3 install -r requirements.txt`

To deactivate venv, run `deactivate`
