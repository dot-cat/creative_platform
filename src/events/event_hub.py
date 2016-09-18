from enum import Enum
from pprint import pprint

from handlers.abs_handler import AbsHandler
from events.abs_message import Message

class Operation(Enum):
    remove = 0
    add = 1


class EventHub(object):
    def __init__(self):
        self.handler_resolver = dict()

    def __process_handler(self, handler: AbsHandler, operation: Operation):
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

                # добавляем или удаляем обработчик для нашего события
                if operation is Operation.add:
                    handlers_available.add(handler)
                else:
                    handlers_available.remove(handler)

    def add_handler(self, handler: AbsHandler):
        self.__process_handler(handler, Operation.add)

    def remove_handler(self, handler: AbsHandler):
        self.__process_handler(handler, Operation.remove)

    def __get_handlers_recursive(self, container: dict, msg_property_iter):
        nested = container.get(next(msg_property_iter))

        if not isinstance(nested, dict):
            return nested
        else:
            return self.__get_handlers_recursive(nested, msg_property_iter)

    def accept_event(self, message: Message):
        types_available = self.handler_resolver

        msg_property_iter = iter(message.get_attributes())

        handlers_available = self.__get_handlers_recursive(types_available, msg_property_iter)

        if handlers_available is None:
            return

        for handler in handlers_available:
            handler.handle(message)
