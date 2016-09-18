##############################################################################################
# FIXME List:
# CC9 - Consider Change 9
#   Возвращать не копию, а ссылку.
##############################################################################################

from events.abs_message import Message
from events.message_pattern import MessagePattern
from copy import copy


class AbsHandler(object):
    def __init__(self, message_pattern: MessagePattern, to_control):
        self.message_pattern = message_pattern
        self.to_control = to_control

    def handle(self, message: Message):
        print(message)

    def get_sensitivity_list(self) -> MessagePattern:
        """
        Получить шаблон перехватываемого сообщения
        :return: EventPattern
        """
        return copy(self.message_pattern)  # CC9
