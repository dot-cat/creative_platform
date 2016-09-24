#!flask/bin/python
from flask import Flask, jsonify, abort, url_for, request

from subsystems.controller_controllables import ControllerControllables
from messages.message_hub import MessageHub
from model import Model

app = Flask(__name__)

objects = [
    {
        "id": "D1",
        "type": "door",
        "actions": ["open", "close"],
        "description": "Entrance door",
        "status": "opened"
    },
    {
        "id": "D2",
        "type": "door",
        "actions": ["open", "close"],
        "description": "to bedroom",
        "status": "opened"
    },
    {
        "id": "D3",
        "type": "door",
        "actions": ["open", "close"],
        "description": "to office",
        "status": "opened"
    },
    {
        "id": "F1",
        "type": "fan",
        "actions": ["on", "off"],
        "description": "",
        "status": "off"
    },
    {
        "id": "Li1",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "on"
    },
    {
        "id": "Li2",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "on"
    },
    {
        "id": "Li3",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "off"
    },
    {
        "id": "Li4",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "off"
    },
    {
        "id": "Li5",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "on"
    },
    {
        "id": "Li6",
        "type": "lighting",
        "actions": ["on", "off"],
        "description": "",
        "status": "off"
    },
    {
        "id": "SB1",
        "type": "sunblind",
        "actions": ["open", "close"],
        "description": "Kitchen",
        "status": "opened"
    },
    {
        "id": "SB2",
        "type": "sunblind",
        "actions": ["open", "close"],
        "description": "Bedroom",
        "status": "opened"
    },
    {
        "id": "SB3",
        "type": "sunblind",
        "actions": ["open", "close"],
        "description": "Office",
        "status": "opened"
    },
    {
        "id": "SB4",
        "type": "sunblind",
        "actions": ["open", "close"],
        "description": "Living Room",
        "status": "opened"
    }
]

model = None
controllables = None
message_hub = None


def init(arg_model: Model, arg_controllables: ControllerControllables, arg_message_hub: MessageHub):
    global model, controllables, message_hub
    model = arg_model
    controllables = arg_controllables
    message_hub = arg_message_hub


def run(*args, **kwargs):
    app.run(*args, **kwargs)


def stop():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/', methods=['GET'])
def get_structure():
    return jsonify({'rooms': url_for('get_rooms'), 'objects': url_for('get_objects')})


@app.route('/rooms/', methods=['GET'])
def get_rooms():
    print(request.headers)
    return jsonify({'rooms': model.get_category_config("rooms")})


@app.route('/room_list/', methods=['GET'])
def get_rooms_list():
    print(request.headers)
    return jsonify(model.get_category_config("rooms"))


@app.route('/rooms/<string:room_id>', methods=['GET'])
def get_room(room_id):
    room = list(filter(lambda t: t['id'] == room_id, model.get_category_config("rooms")))
    if len(room) == 0:
        abort(404)

    print(request.headers)
    return jsonify({'room': room[0]})


@app.route('/objects/', methods=['GET'])
def get_objects():
    print(request.headers)

    return jsonify({'objects': objects})


@app.route('/messages/', methods=['POST'])
def post_message():
    print(request.headers)
    print(request.get_data())
    print(request.get_json())
    return "accepted", 202


@app.route('/objects/<string:object_id>', methods=['GET'])
def get_object(object_id):
    object_item = list(filter(lambda t: t['id'] == object_id, objects))
    if len(object_item) == 0:
        abort(404)

    print(request.headers)
    return jsonify({'object': object_item[0]})
