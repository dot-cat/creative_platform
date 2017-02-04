##############################################################################################
# FIXME List:
# CC14 - Consider Change 14
#   Добавить опциональный параметры: логин и пароль
##############################################################################################

import logging

from mpd import MPDClient
from dpl.connections.abs_connection import Connection, ConnectionFactory

from dpl.connections.connection_registry import ConnectionRegistry


class MPDClientConnection(MPDClient, Connection):
    def __init__(self, host, port, timeout=10, idletimeout=None):  # CC14
        Connection.__init__(self)
        MPDClient.__init__(self)

        self.host = host
        self.port = port
        self.timeout = timeout

        self.idletimeout = idletimeout

        self.__test_connection()

    def __test_connection(self):
        self.connect(self.host, self.port, self.timeout)
        self.disconnect()

    def reconnect(self):
        self.connect(self.host, self.port, self.timeout)

    def __del__(self):
        self.disconnect()


class MPDClientConnectionFactory(ConnectionFactory):
    @staticmethod
    def build(config: dict):
        try:
            return MPDClientConnection(**config["con_params"])
        except ConnectionRefusedError:
            logging.warning("Unable to connect to MPD server %s", config["con_params"])
            return None


ConnectionRegistry.register_factory(
    "mpd_server",
    MPDClientConnectionFactory()
)

