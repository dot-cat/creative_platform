from copy import copy

from handlers.abs_handler import AbsHandler
from events.abs_message import Message


class EventHub(object):
    def __init__(self):
        self.handler_resolver = dict()

    def add_handler(self, handler: AbsHandler):
        # получаем список чувствительности
        message_pattern = handler.get_sensitivity_list()

        # получаем список зарегистрированых типов событий в системе
        types_available = self.handler_resolver

        # получаем список источников сообщений некоторого типа
        sources_available = types_available.get(message_pattern.type, dict())

        # для каждого источника сообщений...
        for source in message_pattern.sources:
            # получаем список событий, которые с ним могут произойти
            events_available = sources_available.get(source, dict())

            # для каждого события...
            for event in message_pattern.events:
                # получаем список его обработчиков
                handlers_available = events_available.get(event, list())

                # добавляем обработчик для нашего изменения
                handlers_available.append(handler)

                # сохраняем новый список обработчиков
                events_available[event] = handlers_available

            # сохраняем новый словарь событий
            sources_available[source] = events_available

        # сохраняем новый словарь источников
        types_available[message_pattern.type] = sources_available

    def remove_handler(self, handler: AbsHandler):
        pass

    def accept_event(self, message: Message):
        types_available = self.handler_resolver

        # FIXME: Копируются только ключи и ссылки. Но все равно топортно
        sources_available = copy(types_available.get(message.type, {}))
        sources_available.update(types_available.get("all", {}))

        if not sources_available:
            return

        events_available = copy(sources_available.get(message.source, {}))
        events_available.update(sources_available.get("all", {}))

        if not events_available:
            return

        handlers_available = copy(events_available.get(message.event, []))
        handlers_available.extend(events_available.get("all", []))

        if not handlers_available:
            return

        for handler in handlers_available:
            handler.handle(message)
