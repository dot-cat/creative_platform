#!flask/bin/python
import logging
import threading
import time

from flask import Flask, jsonify, abort, url_for, request

from dpl.core.config import Config
from dpl.core.message_hub import MessageHub
from dpl.messages.abs_message import Message
from dpl.subsystems.controller_controllables import ControllerControllables

app = Flask(__name__)


def __print_headers():
    logging.debug("Request headers:\n%s", request.headers)

app.before_request(__print_headers)


def init(arg_model: Config, arg_controllables: ControllerControllables, arg_message_hub: MessageHub):
    app.config["model"] = arg_model
    app.config["controllables"] = arg_controllables
    app.config["msg_hub"] = arg_message_hub


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
    return jsonify({'rooms': app.config["model"].get_category_config("rooms")})


@app.route('/rooms/<string:room_id>', methods=['GET'])
def get_room(room_id):
    room = list(filter(lambda t: t['id'] == room_id, app.config["model"].get_category_config("rooms")))
    if len(room) == 0:
        abort(404)

    return jsonify(room[0])


@app.route('/objects/', methods=['GET'])
def get_objects():
    all_info = app.config["controllables"].get_all_objects_info()
    return jsonify({'objects': all_info})


@app.route('/objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
    object_item = None

    try:
        object_item = app.config["controllables"].get_object_info(object_id)
    except ValueError as e:
        if e.args[0] == "id not found":
            abort(404)
        else:
            raise

    return jsonify(object_item)


@app.route('/objects/<string:object_id>/current_track', methods=['GET'])
def get_current_track(object_id):
    object_item = None

    try:
        object_item = app.config["controllables"].do_action(object_id, "get_current_track")
    except ValueError as e:
        if e.args[0] == "id not found":
            abort(404)
        else:
            raise
    except AttributeError:
        abort(404)

    return jsonify(object_item)


@app.route('/messages/', methods=['OPTIONS'])
def messages_options():
    return  '', 204, \
            {'Access-Control-Allow-Methods': 'POST, OPTIONS'}


@app.route('/messages/', methods=['POST'])
def receive_message():
    logging.debug(request.get_data())

    msg_raw = request.get_json()
    if msg_raw is None:
        return jsonify({"result": "Invalid JSON data"}), 400

    logging.debug(msg_raw)

    try:
        msg = Message(
            msg_type=msg_raw["type"],
            source=msg_raw["source"],
            event=msg_raw["event"],
            timestamp=time.time(),
            body=msg_raw["body"]
        )
    except TypeError:
        return jsonify({"result": "Invalid message format"}), 400

    thread = threading.Thread(target=app.config["msg_hub"].accept_msg, args=(msg,))
    thread.start()
    return jsonify({"result": "accepted"}), 202
