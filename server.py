from flask import Flask, send_file, jsonify, request
from flask_cors import CORS

from session_manager import ChatSessionManager
from clientBase import ClientBase
import chatbot
import utils

app = Flask(__name__, static_folder='chatbox')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
csm = ChatSessionManager()
cb = ClientBase()

@app.route('/script')
def serve_js_file():
    js_file_path = './lyxoai-embeder.js'
    return send_file(js_file_path)


@app.route('/chat', methods=["POST"])
def chatCompletion():
    if 'Authorization' not in request.headers:
        return jsonify({'error': 'Authentication Error - API key not provided'})
    authorization_header = request.headers['Authorization']
    _, api_key = authorization_header.split(' ')
    if not cb.api_exists(api_key):
        return jsonify({'error': 'Authentication Error - Invalid API key provided'})

    try:
        data = request.get_json()
        if 'message' in data:
            message = data['message']
            if 'chatSessionId' in data:
                chat_id = data['chatSessionId']
                response_data = chatbot.get_completion(message, chat_id, False, csm)
                response =  jsonify({"reply": response_data, "chatSessionId": chat_id})
                return response
            chat_id = utils.generate_chatid()
            response_data = chatbot.get_completion(message, chat_id, True, csm)
            response = jsonify({"reply": response_data, "chatSessionId": chat_id})
            return response

        return jsonify({'error': 'Invalid request structure'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': f'An error occurred'}), 500


if __name__ == '__main__':
    app.run(debug=True)
