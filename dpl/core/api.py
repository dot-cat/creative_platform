#!flask/bin/python

##############################################################################################
# FIXME List:
# RN1 - Rewrite Now 1
#   Убрать нафиг полный перебор
##############################################################################################


import logging
import threading
import time
import warnings

from flask import Flask, jsonify, abort, url_for, request

from dpl.core.config import Config
from dpl.core.message_hub import MessageHub
from dpl.core.messages.message import Message
from dpl.subsystems.controller_things import ControllerThings

logger = logging.getLogger(__name__)

app = Flask(__name__)

wz_logger = logging.getLogger("werkzeug")
wz_logger.setLevel(logger.getEffectiveLevel())


def __print_headers():
    logger.debug("Request headers:\n%s", request.headers)

app.before_request(__print_headers)


def init(arg_model: Config, arg_things: ControllerThings, arg_message_hub: MessageHub):
    app.config["model"] = arg_model
    app.config["things"] = arg_things
    app.config["msg_hub"] = arg_message_hub


def run(*args, **kwargs):
    app.run(*args, **kwargs)


@app.route('/', methods=['GET'])
def get_structure():
    return jsonify(
        {
            'rooms': url_for('get_rooms'),
            'objects': url_for('get_objects'),
            'things': url_for('get_things'),
            'messages': url_for('receive_message')
        }
    )


@app.route('/rooms/', methods=['GET'])
def get_rooms():
    return jsonify({'rooms': app.config["model"].get_category_config("rooms")})


@app.route('/rooms/<string:room_id>', methods=['GET'])  # Fixme: RN1
def get_room(room_id):
    room = list(filter(lambda t: t['id'] == room_id, app.config["model"].get_category_config("rooms")))
    if len(room) == 0:
        abort(404)

    return jsonify(room[0])


@app.route('/objects/', methods=['GET'])
def get_objects():
    warnings.warn(
        "This route will be replaced with /things/ route",
        PendingDeprecationWarning
    )
    all_info = app.config["things"].get_all_objects_info()
    return jsonify({'objects': all_info})


@app.route('/objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
    warnings.warn(
        "This route will be replaced with /things/<string:object_id> route",
        PendingDeprecationWarning
    )
    object_item = None

    try:
        object_item = app.config["things"].get_object_info(object_id)
    except ValueError as e:
        if e.args[0] == "id not found":
            abort(404)
        else:
            raise

    return jsonify(object_item)


@app.route('/objects/<string:object_id>/current_track', methods=['GET'])
def get_current_track(object_id):
    warnings.warn(
        "This route will be removed in v0.4. "
        "All needed information is moved to extended_info attribute",
        PendingDeprecationWarning
    )
    object_item = None

    try:
        object_item = app.config["things"].do_action(object_id, "get_current_track")
    except ValueError as e:
        if e.args[0] == "id not found":
            abort(404)
        else:
            raise
    except AttributeError:
        abort(404)

    return jsonify(object_item)


@app.route('/things/', methods=['GET'])
def get_things():
    things_container = app.config["things"]  # type: ControllerThings
    all_info = things_container.get_all_things_info()
    return jsonify({'things': all_info})


@app.route('/things/<string:thing_id>', methods=['GET'])  # Fixme: RN1
def get_thing(thing_id):
    object_item = None
    things_container = app.config["things"]  # type: ControllerThings

    try:
        object_item = things_container.get_thing_info(thing_id)
    except ValueError as e:
        if e.args[0] == "id not found":
            abort(404)
        else:
            raise

    return jsonify(object_item)


@app.route('/messages/', methods=['OPTIONS'])
def messages_options():
    return  '', 204, \
            {'Access-Control-Allow-Methods': 'POST, OPTIONS'}


@app.route('/messages/', methods=['POST'])
def receive_message():
    logger.debug(request.get_data())

    msg_raw = request.get_json()
    if msg_raw is None:
        return jsonify({"result": "Invalid JSON data"}), 400

    logger.debug(msg_raw)

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
