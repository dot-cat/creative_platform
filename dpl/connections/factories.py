import logging

from dpl.connections.shift_reg_buffered import ShiftRegBuffered
from dpl.connections.shift_reg_gpio import ShiftRegGPIO
from dpl.connections.mpd_client import MPDClientConnection


def get_connection_by_config(config) -> object:
    connection = None

    if config["con_type"] == "shiftreg":
        connection = \
            ShiftRegBuffered(
                ShiftRegGPIO(**config["con_params"])
            )
    elif config["con_type"] == "mpd_server":
        try:
            connection = \
                MPDClientConnection(**config["con_params"])
        except ConnectionRefusedError:
            logging.warning("Unable to connect to MPD server {0}".format(config["con_params"]))
    else:
        logging.warning("Unknown connection: {0}".format(config))

    return connection
