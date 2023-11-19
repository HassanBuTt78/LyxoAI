from flask import Flask, send_file, jsonify, request, render_template
from flask_cors import CORS

from .clientBase import ClientBase
from .session_manager import ChatSessionManager

from . import chatbot
from . import utils


app = Flask(__name__, static_folder='static')
csm = ChatSessionManager()
cb = ClientBase()
origins = cb.get_all_domains()
cors = CORS(app, resources={r"/*": {"origins": origins}})


def update_cors_domains():
    origins = cb.get_all_domains()
    cors = CORS(app, resources={r"/*": {"origins": origins}})


@app.route('/script/<id>')
def serve_js_file(id):
    if not id:
        return '', 404
    return render_template('script-temp.js', id=id)


@app.route('/')
def home():
    return send_file('./LandingPage/home.html')


@app.route('/widget/<widget_id>')
def send_widget(widget_id):
    if request.headers.get('sec-fetch-dest') != 'iframe':
        return ''
    data = cb.get_user_info(widget_id)
    if data is None:
        return '', 404

    response = render_template(data["widget"]["template"], data=data)
    return response


@app.route('/chat', methods=["POST"])
def chatCompletion():
    print('request Recieved')
    auth = utils.authenticate_request(request, cb)
    if 'error' in auth:
        return jsonify(auth), 403
    system_prompt = auth['system_prompt']
    try:
        data = request.get_json()
        if 'message' in data:
            message = data['message']
            chat_id = request.cookies.get('chatSessionId')
            if chat_id:
                response_data = chatbot.get_completion(
                    message, chat_id, False, system_prompt, csm)
                response = jsonify({"reply": response_data})
                return response
            chat_id = utils.generate_chatid()
            response_data = chatbot.get_completion(
                message, chat_id, True, system_prompt, csm)
            response = jsonify({"reply": response_data})
            response.set_cookie('chatSessionId', chat_id, max_age=1800)
            return response

        return jsonify({'error': 'Invalid request structure'}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': f'An error occurred'}), 500


if __name__ == '__main__':
    update_cors_domains()
    app.run(debug=True)
