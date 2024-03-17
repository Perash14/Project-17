from enum import Enum
import signal
import sys
from db import ChatDB
import socket
import threading
import json


class Actions(Enum):
    INSERT_USER=1
    SEND_MESSAGE=2
    GET_MESSAGES = 3


chat_DAL = ChatDB()


clients = {}


def insertUser(payload):

    username = payload.get('username')
    room_number = payload.get('room_number')
    return chat_DAL.insert_user(username,room_number)

def sendMessage(payload):
    userid = payload.get('user_id')
    message = payload.get('message')
    print(payload)
    chat_DAL.add_message(message,userid)

def getMessages(payload):
    room_number = payload.get('room_number')
    messages = chat_DAL.get_messages(room_number)
    return messages

def handle_client(client_socket):
    try:
        print(client_socket)
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print("received from client ",data)
            data_serialized = json.loads(data)
           
            match data_serialized.get('action'):
                case Actions.INSERT_USER.value:
                    user_id = insertUser(data_serialized)
                    clients[client_socket]= data_serialized
                    
                    send_message_to_client(client_socket,Actions.INSERT_USER,user_id=user_id)
                case Actions.SEND_MESSAGE.value:
                    sendMessage(data_serialized.get('payload'))
                    messages = getMessages(data_serialized.get('payload'))
                    room_number = data_serialized.get('payload').get('room_number')
                    for client, client_data in clients.items():
                        if client!=client_socket and client_data.get('room_number') == room_number:
                            send_message_to_client(client,Actions.GET_MESSAGES,messages=messages)
    except Exception as e:
        print(f"Error in handling clients : ${e}")

        
    
    # if client_socket in clients:
    #     del clients[client_socket]
    #client_socket.close()
def send_message_to_client(client_socket,action,**kwargs):
    try:
        print('sendmessagetoclient')
        message = {"action":action.value}
        message.update(kwargs)
        json_message = json.dumps(message)
        print(json_message)
        client_socket.send(json_message.encode('utf-8'))
    except Exception as e:
        print(f"Error while sending message: {e}")


def create_server():
    signal.signal(signal.SIGINT,signal_handler)
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('localhost',3000))
    server_socket.listen(20)
    print("Server is listening on port:3000")
    while True:
        client_socket,client_address = server_socket.accept()
        #print("Client connected: ",client_socket.getpeername())
        print(client_socket)
        client_thread = threading.Thread(target=handle_client,args=(client_socket,))
        client_thread.start()

def signal_handler(sig,frame):
    print("CTRL + C pressed, exiting...")
    sys.exit(0)

if __name__=="__main__":
    create_server()
    