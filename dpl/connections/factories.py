import logging

from dpl.connections.mpd_client import MPDClientConnection
from dpl.connections.shift_reg_buffered import ShiftRegBuffered
from dpl.connections.shift_reg_gpio import ShiftRegGPIO


def get_connection_by_config(config) -> object:
    if config["con_type"] == "shiftreg":
        return ShiftRegBuffered(
            ShiftRegGPIO(**config["con_params"])
        )
    elif config["con_type"] == "mpd_server":
        try:
            return MPDClientConnection(**config["con_params"])
        except ConnectionRefusedError:
            logging.warning("Unable to connect to MPD server %s", config["con_params"])
    else:
        logging.warning("Unknown connection: %s", config)

    return None
