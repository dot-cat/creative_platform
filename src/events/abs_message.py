import time


class Message(object):
    def __init__(self, type, source, event, timestamp: time, body):
        self.type = type
        self.source = source
        self.event = event
        self.timestamp = timestamp
        self.body = body

    def dump_dict(self):
        return dict(self.__dict__)
