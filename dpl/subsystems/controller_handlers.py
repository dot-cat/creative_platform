from dpl.handlers.handler_scenarios import HandlerScenarios, HandleActions, MessagePattern
from dpl.handlers.user_request_handler import UserRequestHandler
from dpl.messages.message_hub import MessageHub
from dpl.model import Model


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
            h_id = item["id"]
            h_if = item["if"]
            pattern = MessagePattern(
                msg_type=h_if["type"],
                source_list=h_if["source_list"],
                event_list=h_if["event_list"]
            )

            if pattern.type == "user_request":
                self.all_handlers[h_id] = UserRequestHandler(
                    pattern, controllables
                )
            else:
                hconfig = HandleActions()
                hconfig.add_action(**item["then"])
                self.all_handlers[h_id] = HandlerScenarios(pattern, controllables, hconfig)

    def register_all_handlers(self, msg_hub: MessageHub):
        for handler in self.all_handlers.values():
            msg_hub.add_handler(handler)
