#!flask/bin/python
from flask import Flask, jsonify, abort, url_for, request
import time
import logging
import threading

from subsystems.controller_controllables import ControllerControllables
from messages.message_hub import MessageHub
from messages.abs_message import Message
from model import Model

app = Flask(__name__)



model = None
controllables = None
message_hub = None


def __print_headers():
    logging.debug("Request headers:\n{0}".format(request.headers))

app.before_request(__print_headers)


def init(arg_model: Model, arg_controllables: ControllerControllables, arg_message_hub: MessageHub):
    global model, controllables, message_hub
    model = arg_model
    controllables = arg_controllables
    message_hub = arg_message_hub


def run(*args, **kwargs):
    app.run(*args, **kwargs)


@app.route('/', methods=['GET'])
def get_structure():
    return jsonify(
        {
            'rooms': url_for('get_rooms'),
            'objects': url_for('get_objects'),
            'messages': url_for('receive_message')
        }
    )


@app.route('/rooms/', methods=['GET'])
def get_rooms():
    return jsonify({'rooms': model.get_category_config("rooms")})


@app.route('/rooms/<string:room_id>', methods=['GET'])
def get_room(room_id):
    room = list(filter(lambda t: t['id'] == room_id, model.get_category_config("rooms")))
    if len(room) == 0:
        abort(404)

    return jsonify(room[0])


@app.route('/objects/', methods=['GET'])
def get_objects():
    all_info = controllables.get_all_objects_info()
    return jsonify({'objects': all_info})


@app.route('/objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
    object_item = None

    try:
        object_item = controllables.get_object_info(object_id)
    except KeyError:
        abort(404)

    return jsonify(object_item)


@app.route('/messages/', methods=['POST'])
def receive_message():
    logging.debug(request.get_data())

    msg_raw = request.get_json()
    if msg_raw is None:
        return "Invalid JSON data", 400

    logging.debug(msg_raw)
    msg_raw["timestamp"] = time.time()

    try:
        msg = Message(**msg_raw)
    except TypeError:
        return "Invalid message format", 400

    thread = threading.Thread(target=message_hub.accept_msg, args=(msg,))
    thread.start()
    return "accepted", 202
