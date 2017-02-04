from dpl.handlers.abs_handler import AbsHandler, Message, MessagePattern
from dpl.handlers.handle_config import HandleConfig, ActionItem


class ConfHandler(AbsHandler):
    def __init__(self, handle_config: HandleConfig, message_pattern: MessagePattern, to_control):
        """
        Настраиваемый Handler. Позволяет указать логику работы метода handle()
        с помощью конфига
        :param handle_config: конфиг, задающий логику работы ф-ции матода()
        :param message_pattern: шаблон выборки сообщений
        :param to_control: объект, над которым будут выполняться действия в методе handle
        """
        super().__init__(message_pattern, to_control)

        self.handle_config = handle_config

    def handle(self, message: Message):
        for action in self.handle_config.get_actions():
            self.to_control.do_action(action.obj_id, action.obj_action, action.action_args)
