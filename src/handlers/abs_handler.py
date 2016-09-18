##############################################################################################
# FIXME List:
# CC9 - Consider Change 9
#   Возвращать не копию, а ссылку.
##############################################################################################

from events.abs_message import Message
from events.message_pattern import MessagePattern
from copy import copy


class AbsHandler(object):
    """
    Handler - объект, который выполняет некоторые действия в ответ на принятое сообщение.
    """
    def __init__(self, message_pattern: MessagePattern, to_control):
        """
        Конструктор
        :param message_pattern: шаблон выборки сообщений
        :param to_control: объект, над которым будут выполняться действия в методе handle
        """
        self.message_pattern = message_pattern
        self.to_control = to_control

    def handle(self, message: Message):
        """
        Обработка сообщения и выполнение ответных действий
        :param message: сообщение
        :return: None
        """
        raise NotImplementedError

    def get_sensitivity_list(self) -> MessagePattern:
        """
        Получить шаблон перехватываемого сообщения
        :return: EventPattern
        """
        return copy(self.message_pattern)  # CC9
