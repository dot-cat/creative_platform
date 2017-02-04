from dpl.handlers.abs_handler import AbsHandler, Message, MessagePattern
from dpl.handlers.handle_actions import HandleActions


class HandlerScenarios(AbsHandler):
    def __init__(self, message_pattern: MessagePattern, to_control, actions: HandleActions):
        """
        Handler для сценариев. Позволяет указать логику работы метода handle()
        с помощью конфига
        :param message_pattern: шаблон выборки сообщений
        :param to_control: объект, над которым будут выполняться действия в методе handle
        :param actions: конфиг, задающий список выполняемых действий
        """
        super().__init__(message_pattern, to_control)

        self.actions = actions

    def handle(self, message: Message):
        for action in self.actions.get_actions():
            self.to_control.do_action(action.obj_id, action.obj_action, action.action_args)
