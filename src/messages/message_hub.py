##############################################################################################
# FIXME List:
# CB1 - Critically Bad 1
#   Код в этом файле оставляет желать лучшего. Перепеписать как можно скорее!
#   Конкретно:
#   * использовать рекурсию вместо вложенных циклов;
#   * уменьшить дублирование кода;
#   * предусмотреть обработку сообщений с изменившимся количеством параметров.
#   Для этого можно использовать наработки из веток alt_accept_handler и alternative_resolver.
##############################################################################################


from enum import Enum
import logging
from threading import Thread

from handlers.abs_handler import AbsHandler


class Operation(Enum):
    remove = 0
    add = 1


class MessageHub(object):
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

    def accept_msg(self, message):
        logging.debug("Accepted message: {0}".format(message))
        logging.debug("{0}".format(message.dump_dict()))

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
            handler_thread = Thread(target=handler.handle, args=(message,))
            handler_thread.run()
