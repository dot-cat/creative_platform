import logging

from connections.shift_reg_buffered import ShiftRegBuffered
from connections.shift_reg_gpio import ShiftRegGPIO


def get_connection_by_config(config) -> object:
    connection = None

    if config["con_type"] == "shiftreg":
        connection = \
            ShiftRegBuffered(
                ShiftRegGPIO(**config["con_params"])
            )
    else:
        logging.warning("Unknown connection: {0}".format(config))

    return connection
