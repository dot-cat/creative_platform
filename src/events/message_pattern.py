class MessagePattern(object):
    def __init__(self, type, source_list: list, event_list: list):
        self.type = type
        self.sources = source_list
        self.events = event_list

    def dump_dict(self):
        return dict(self.__dict__)
