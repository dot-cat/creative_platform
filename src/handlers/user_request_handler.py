##############################################################################################
# FIXME List:
# CC11 - Consider Change 11
#   Проверять права на исполнение
##############################################################################################


from handlers.abs_handler import AbsHandler, MessagePattern, Message
from subsystems.controller_controllables import ControllerControllables


class UserRequestHandler(AbsHandler):
    def __init__(self, message_pattern: MessagePattern, to_control: ControllerControllables):
        super().__init__(message_pattern, to_control)

    def handle(self, message: Message):
        self.to_control.do_action(**message.body)  # CC11
