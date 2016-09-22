from collections.abc import Iterable


class MessagePattern(object):
    def __init__(self, type, source_list: Iterable, event_list: Iterable):
        """
        Шаблон выборки сообщений - структура, которая содержит:
        :param type: тип сообщения
        :param source_list: список идентификаторов источников
        :param event_list: список идентификаторов событий
        """
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
        """
        Вернуть словарь, содержащий все возможные значения всех атрибутов сообщения
        :return: словарь
        """
        return dict(self.__dict__)
