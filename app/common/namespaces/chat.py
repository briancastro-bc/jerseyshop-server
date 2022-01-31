import socketio

class ChatNamespace(socketio.AsyncNamespace):
    
    async def on_connect(self):
        print('Connected')