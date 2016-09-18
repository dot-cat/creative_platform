from handlers.abs_handler import AbsHandler


class EventHub(object):
    def __init__(self):
        self.handler_resolver = dict()

    def add_handler(self, handler: AbsHandler):
        # получаем список чувствительности
        sens_pattern = handler.get_sensitivity_list()

        # получаем список зарегистрированых типов событий в системе
        sources_by_type = self.handler_resolver

        # получаем список источников сообщений некоторого типа, существующий или новый
        events_by_source = sources_by_type.setdefault(sens_pattern.type, dict())

        # для каждого источника сообщений...
        for source in sens_pattern.sources:
            # получаем список событий, которые с ним могут произойти, существующий или новый
            handlers_by_event = events_by_source.setdefault(source, dict())

            # для каждого события...
            for event in sens_pattern.events:
                # получаем список его обработчиков, существующий или новый
                handlers_available = handlers_by_event.setdefault(event, set())

                # добавляем обработчик для нашего изменения
                handlers_available.add(handler)

    def remove_handler(self, handler: AbsHandler):
        # получаем список чувствительности
        sens_pattern = handler.get_sensitivity_list()

        # получаем список зарегистрированых типов событий в системе
        types_available = self.handler_resolver

        # получаем список источников сообщений некоторого типа
        sources_available = types_available.get(sens_pattern.type, dict())

        # для каждого источника сообщений...
        for source in sens_pattern.sources:
            # получаем список событий, которые с ним могут произойти
            events_available = sources_available.get(source, dict())

            # для каждого события...
            for event in sens_pattern.events:
                # получаем список его обработчиков
                handlers_available = events_available.get(event, set())

                # удаляем обработчик для нашего изменения
                handlers_available.remove(handler)

                # сохраняем новый список обработчиков
                events_available[event] = handlers_available

            # сохраняем новый словарь событий
            sources_available[source] = events_available

        # сохраняем новый словарь источников
        types_available[sens_pattern.type] = sources_available

    def accept_event(self, message):
        types_available = self.handler_resolver

        sources_available = types_available.get(message.type)
        if sources_available is None:
            return

        events_available = sources_available.get(message.source)

        if events_available is None:
            return

        handlers_available = events_available.get(message.event)

        if handlers_available is None:
            return

        for handler in handlers_available:
            handler.handle(message)
