from db import ChatDB
from flask import Flask, jsonify, request

app  = Flask(__name__)

messages = []


chat_DAL = ChatDB()
@app.route('/user',methods=['POST'])
def insert_user():
    try:
        response = request.get_json()
        userid =  chat_DAL.insert_user(response['username'])
        return jsonify(userid)
    except ValueError as e:
        return jsonify(e)

  

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = chat_DAL.get_messages()
    return jsonify(messages)

@app.route('/messages'
           , methods=['POST'])
def recieve_message():
    try:
        new_message = request.get_json()
        chat_DAL.add_message(new_message['message'],new_message['userid'])
        return jsonify('ok')
    except ValueError as e :
        return jsonify(e)




if __name__ == '__main__':
    app.run(debug=True)