from handlers.abs_handler import AbsHandler


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

    def remove_handler(self, handler):
        pass

    def accept_event(self, message):
        types_available = self.handler_resolver

        sources_available = types_available.get(message.type)
        if sources_available is None:
            return

        events_available = sources_available.get(message.source)

        if events_available is None:
            return

        handlers_available = events_available.get(message.event)

        if events_available is None:
            return

        for handler in handlers_available:
            handler.handle(message)
