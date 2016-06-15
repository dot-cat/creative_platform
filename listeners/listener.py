class Listener(object):
    def __init__(self):
        pass

    def __del__(self):
        raise NotImplementedError

    def __data_waiter(self):
        raise NotImplementedError

    def __handler(self, event):
        raise NotImplementedError
