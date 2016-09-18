from collections.abc import Iterable


class MessagePattern(object):
    def __init__(self, type, source_list: Iterable, event_list: Iterable):
        if not isinstance(source_list, Iterable):
            raise ValueError("source_list must be iterable")

        if not isinstance(event_list, Iterable):
            raise ValueError("event_list must be iterable")

        # Если список пустой...
        if not source_list:
            raise ValueError("source_list can't be empty")

        if not event_list:
            raise ValueError("event_list can't be empty")

        self.type = type
        self.sources = source_list
        self.events = event_list

    def dump_dict(self):
        return dict(self.__dict__)

    def get_attributes(self) -> tuple:
        """
        Вернуть кортеж атрибутов в порядке уменьшения важности
        :return: tuple, кортеж атрибутов объекта
        """
        return self.type, self.sources, self.events
