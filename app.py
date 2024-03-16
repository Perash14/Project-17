from flask import Flask, jsonify, request

app  = Flask(__name__)

messages = []

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def recieve_message():
    new_message = request.get_json()
    messages.append(new_message)
    return jsonify(new_message)

if __name__ == '__main__':
    app.run(debug=True)