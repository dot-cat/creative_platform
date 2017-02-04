import time


class Message(object):
    def __init__(self, msg_type, source, event, timestamp: time, body):
        """
        Сообщение - структура, которая содержит:
        :param msg_type: тип сообщения (например player, button, sensor и т.д.)
        :param source: идентификатор источника сообщения
        :param event: событие, которое произошло (pressed, stopped и т.д.)
        :param timestamp: время формирования сообщения
        :param body: тело сообщения, дополнительная информацию
        """
        self.type = msg_type
        self.source = source
        self.event = event
        self.timestamp = timestamp
        self.body = body

    def dump_dict(self) -> dict:
        """
        Вернуть словарь, содержащий значения всех атрибутов сообщения
        :return: словарь
        """
        return dict(self.__dict__)
