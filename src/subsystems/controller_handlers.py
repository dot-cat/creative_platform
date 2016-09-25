from handlers.conf_handler import ConfHandler, HandleConfig, Message, MessagePattern
from handlers.user_request_handler import UserRequestHandler
from messages.message_hub import MessageHub
from model import Model


class ControllerHandlers(object):
    def __init__(self, model: Model, controllables):
        self.model = model

        self.__init_handlers(controllables)

    def __del__(self):
        self.all_handlers.clear()

    def __init_handlers(self, controllables):
        self.all_handlers = dict()

        handler_data_list = self.model.get_category_config("handlers")

        for item in handler_data_list:
            id = item["id"]
            pattern = MessagePattern(**item["if"])

            if pattern.type == "user_request":
                self.all_handlers[id] = UserRequestHandler(
                    pattern, controllables
                )
            else:
                hconfig = HandleConfig()
                hconfig.add_action(**item["then"])
                self.all_handlers[id] = ConfHandler(
                    hconfig, pattern, controllables
                )

    def register_all_handlers(self, msg_hub: MessageHub):
        for handler in self.all_handlers.values():
            msg_hub.add_handler(handler)
