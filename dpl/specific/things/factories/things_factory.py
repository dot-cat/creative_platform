import logging

from dpl.core.things import Thing
from dpl.specific.things.factories import (
    get_slider_by_params,
    get_trigger_by_params,
    get_player_by_params
)


def get_things_by_params(con_instance, con_params, metadata) -> Thing:
    item_type = metadata["type"]

    if item_type == "door" or item_type == "sunblind":
        return get_slider_by_params(con_instance, con_params, metadata)
    elif item_type == "lighting" or item_type == "fan":
        return get_trigger_by_params(con_instance, con_params["sr_pin"], metadata)
    elif item_type == "player":
        return get_player_by_params(con_instance, con_params, metadata)
    else:
        logging.warning("Unknown type of object: {0}".format(item_type))

    return None
