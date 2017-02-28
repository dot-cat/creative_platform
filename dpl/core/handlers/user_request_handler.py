##############################################################################################
# FIXME List:
# CC11 - Consider Change 11
#   Проверять права на исполнение
##############################################################################################

import logging

from dpl.core.handlers.abs_handler import AbsHandler, MessagePattern, Message
from dpl.subsystems.controller_things import ControllerThings

LOGGER = logging.getLogger(__name__)


class UserRequestHandler(AbsHandler):
    def __init__(self, message_pattern: MessagePattern, to_control: ControllerThings):
        super().__init__(message_pattern, to_control)

    def handle(self, message: Message):
        returned = self.to_control.do_action(**message.body)  # CC11
        LOGGER.debug(
            "Handler caught command: %s. "
            "CMD returned: %s",
            message.body["action"],
            returned
        )
