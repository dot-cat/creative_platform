import logging

from model import Model

from controllable_objects.factories.slider_factory import get_slider_by_params
from controllable_objects.factories.trigger_factory import get_trigger_by_params
from connections.factories import get_connection_by_config


class ControllerControllables(object):
    def __init__(self, model_data):
        self.model_data = model_data

        self.__init_all_connections()
        self.__init_all_controllables()

    def __del__(self):
        self.all_controllables.clear()
        self.all_connections.clear()

    def __init_all_connections(self):
        self.all_connections = dict()

        con_data_list = self.model_data["connections"]

        for item in con_data_list:
            if item["con_type"] == "shiftreg":
                self.all_connections[item["id"]] = \
                    get_connection_by_config(item)

    def __init_all_controllables(self):
        self.all_controllables = dict()

        for item in self.model_data["controllables"]:
            con_instance = self.all_connections[item["con_id"]]
            con_params = item["con_params"]

            if item["type"] == "door" or item["type"] == "sunblind":
                self.all_controllables[item["id"]] = get_slider_by_params(con_instance, con_params)

            elif item["type"] == "lighting" or item["type"] == "fan":
                self.all_controllables[item["id"]] = get_trigger_by_params(con_instance, con_params["sr_pin"])

    def __resolve_obj_by_id(self, obj_id: str):
        if type(obj_id) != str:
            raise ValueError('Value must be a string literal')

        if obj_id not in self.all_controllables:
            raise ValueError('id not found')

        return self.all_controllables[obj_id]

    def toggle_controllable(self, obj_id):
        """
        Функция для переключения объекта в противоположное состояние
        :param obj_id: идентификатор объекта
        :return: True - успешно, False - неуспешно
        """
        obj_alias = self.__resolve_obj_by_id(obj_id)

        obj_alias.toggle()

        return True

    def check_action_permitted(self, obj_id: str, action: str, action_params):
        # FIXME: TD2, Проверка прав на выполнение действия
        logging.warning("Permission checking is not implemented")
        pass

    def do_action(self, obj_id: str, action: str, action_params=()):
        """
        Функция для выполнения действия на объекте
        :param obj_id: тип объекта
        :param action: действие, метод, который необходимо вызвать на объекте
        :param action_params: параметры вызова
        :return: None  # CC7
        """
        # FIXME: TD1
        self.check_action_permitted(obj_id, action, action_params)

        obj_alias = self.__resolve_obj_by_id(obj_id)

        try:
            method_to_call = getattr(obj_alias, action)
            method_to_call(*action_params)
        except AttributeError:
            raise
