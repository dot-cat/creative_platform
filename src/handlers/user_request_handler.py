##############################################################################################
# FIXME List:
# CC11 - Consider Change 11
#   Проверять права на исполнение
##############################################################################################


from handlers.abs_handler import AbsHandler, MessagePattern, Message

user_request_pattern = MessagePattern(
    "user_request",
    ["cli"],
    ["action_requested"]
)


class UserRequestHandler(AbsHandler):
    def __init__(self, to_control):
        super().__init__(user_request_pattern, to_control)

    def handle(self, message: Message):
        self.to_control.do_action(**message.body)  # CC11
