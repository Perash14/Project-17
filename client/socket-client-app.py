from enum import Enum
import socket
import json
import threading




class Actions(Enum):
    INSERT_USER=1
    SEND_MESSAGE=2
    GET_MESSAGES=3


user_id = -1

def insert_user(client_socket,username,room_number):
    
    payload ={'action':Actions.INSERT_USER.value,'username':username,'room_number':room_number}
    payload = json.dumps(payload)
    client_socket.send(payload.encode('utf-8'))
    
    

def showMessages(messages):
    for message in messages:
        print(f"{message[0]}:{message[1]}")

def handle_receive_message(data):
     global user_id
     action = data.get('action')
     if action == Actions.INSERT_USER.value:
        user_id = data.get('user_id') 
       
     elif action == Actions.GET_MESSAGES.value:
        
         messages = data.get('messages')
         showMessages(messages)
    
    
def receive_message(client_socket):
        global user_id
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            data_serialized = json.loads(data)
            handle_receive_message(data_serialized)


def start_client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect(('localhost',3000))
    username = input('Enter your username: ')
    # Choose to implement chosen 'known' rooms instead of implementing room displaying list display as it was not requested
    room_number = input('Enter your room number: ')
    insert_user(client_socket,username, room_number)
    receive_thread = threading.Thread(target=receive_message,args=(client_socket,))
    receive_thread.start()
    


    while True:
            if user_id != -1:
                text = input('Enter your message: ')
                message = {"user_id": user_id, "message": text,"room_number":room_number}
                message_action = json.dumps({'action':Actions.SEND_MESSAGE.value,'payload':message})
                client_socket.send(message_action.encode('utf-8'))

if __name__ == "__main__":
    start_client()