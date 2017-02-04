from collections import namedtuple


ActionItem = namedtuple("ActionItem", ("obj_id", "obj_action", "action_args"))


class HandleActions(object):
    def __init__(self):
        """
        Класс, обеспечивающий конфигурацию метода handle
        """
        self.obj_actions = list()

    def add_action(self, obj_id, obj_action: str, action_args=()) -> None:
        """
        Добавление действия над объектом
        :param obj_id: идентификатор объекта, над которым производится действие
        :param obj_action: вызываемый метод объекта
        :param action_args: аргументы действия
        :return: None
        """
        self.obj_actions.append(ActionItem(obj_id, obj_action, action_args))

    def get_actions(self) -> list:
        return self.obj_actions
