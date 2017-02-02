from dpl.core.config import Config
from dpl.core.message_hub import MessageHub
from dpl.handlers.factories import get_handler_by_config


class ControllerHandlers(object):
    def __init__(self, model: Config, things):
        self.model = model

        self.__init_handlers(things)

    def __del__(self):
        self.all_handlers.clear()

    def __init_handlers(self, things):
        self.all_handlers = dict()

        handler_data_list = self.model.get_category_config("handlers")

        for item in handler_data_list:
            self.all_handlers[item["id"]] = get_handler_by_config(item, things)

    def register_all_handlers(self, msg_hub: MessageHub):
        for handler in self.all_handlers.values():
            msg_hub.add_handler(handler)
