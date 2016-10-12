##############################################################################################
# FIXME List:
# CC14 - Consider Change 14
#   Добавить опциональный параметры: логин и пароль
##############################################################################################


from mpd import MPDClient


class MPDClientConnection(MPDClient):
    def __init__(self, host, port, timeout=10, idletimeout=None):  # CC14
        super().__init__()

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
