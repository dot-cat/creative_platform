import logging

from controllable_objects.abstract.abs_controllable import AbsControllable
from controllable_objects.factories.slider_factory import get_slider_by_params
from controllable_objects.factories.trigger_factory import get_trigger_by_params
from controllable_objects.factories.player_factory import get_player_by_params


def get_controllable_by_params(con_instance, con_params, metadata) -> AbsControllable:
    item_type = metadata["type"]

    new_obj = None

    if item_type == "door" or item_type == "sunblind":
        new_obj = get_slider_by_params(con_instance, con_params, metadata)
    elif item_type == "lighting" or item_type == "fan":
        new_obj = get_trigger_by_params(con_instance, con_params, metadata)
    elif item_type == "player":
        new_obj = get_player_by_params(con_instance, con_params, metadata)
    else:
        logging.warning("Unknown type of object: {0}".format(item_type))

    return new_obj
