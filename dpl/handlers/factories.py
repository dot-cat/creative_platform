from dpl.handlers.user_request_handler import UserRequestHandler
from dpl.handlers.handle_actions import HandleActions
from dpl.handlers.handler_scenarios import HandlerScenarios
from dpl.messages.message_pattern import MessagePattern


def get_handler_by_config(config: dict, things: object) -> object:
    h_id = config["id"]
    h_if = config["if"]
    pattern = MessagePattern(
        msg_type=h_if["type"],
        source_list=h_if["source_list"],
        event_list=h_if["event_list"]
    )

    if pattern.type == "user_request":
        return UserRequestHandler(
            pattern, things
        )
    else:
        hconfig = HandleActions()
        hconfig.add_action(**config["then"])
        return HandlerScenarios(pattern, things, hconfig)
