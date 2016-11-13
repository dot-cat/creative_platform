import logging
import serial

from connections.shift_reg_buffered import ShiftRegBuffered
from connections.shift_reg_gpio import ShiftRegGPIO
from connections.mpd_client import MPDClientConnection


def get_connection_by_config(config) -> object:
    connection = None

    con_type = config["con_type"]

    if con_type == "shiftreg":
        connection = \
            ShiftRegBuffered(
                ShiftRegGPIO(**config["con_params"])
            )

    elif con_type == "mpd_server":
        try:
            connection = \
                MPDClientConnection(**config["con_params"])
        except ConnectionRefusedError:
            logging.warning("Unable to connect to MPD server {0}".format(config["con_params"]))

    elif con_type == "serial":
        tty = config["con_params"]["tty"]

        try:
            connection = serial.Serial(tty)
            connection.baudrate = config["con_params"]["baudrate"]
        except serial.SerialException:
            logging.warning("Unable to init {0} connection: {1} is disconnected".format(config["id"], tty))

    else:
        logging.warning("Unknown connection: {0}".format(config))

    return connection
