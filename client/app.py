import requests
import time
import threading
import os

def get_messages():
    base_url = os.environ.get("CHAT_API_BASE_URL", "http://localhost:5000")
    response = requests.get(f'{base_url}/messages')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_message(message):
    base_url = os.environ.get("CHAT_API_BASE_URL", "http://localhost:5000")
    response = requests.post(f'{base_url}/messages', json=message)
    if response.status_code != 200:
        print('error: failed to send message')
        
def poll_messages():
    while True:
        messages = get_messages()
        print(messages)
        time.sleep(1)

def main_loop():
    username = input('Enter your username: ')
    polling_messages = threading.Thread(target=poll_messages)
    polling_messages.start()
    try:
        while True:
            text = input('Enter your message: ')
            message = {"username": username, "text": text}
            send_message(message)
    finally:
        polling_messages.join()

if __name__ == "__main__":
    main_loop()