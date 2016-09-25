##############################################################################################
# FIXME List:
# TD3 - To Do 3
#   Переписать метод get_permitted_actions, добавить проверку пользователя, обработку
#   дополнительных условий.
# CC13 - Consider Change 13
#   Кешировать информацию об объектах.
##############################################################################################

import logging

from model import Model

from controllable_objects.abstract.abs_controllable import AbsControllable
from controllable_objects.factories.slider_factory import get_slider_by_params, AbsSlider
from controllable_objects.factories.trigger_factory import get_trigger_by_params, AbsTrigger
from connections.factories import get_connection_by_config


class ControllerControllables(object):
    def __init__(self, model: Model):
        self.model = model

        self.__init_all_connections()
        self.__init_all_controllables()

    def __del__(self):
        self.all_controllables.clear()
        self.all_connections.clear()

    def __init_all_connections(self):
        self.all_connections = dict()

        con_data_list = self.model.get_category_config("connections")

        for item in con_data_list:
            if item["con_type"] == "shiftreg":
                self.all_connections[item["id"]] = \
                    get_connection_by_config(item)

    def __init_all_controllables(self):
        self.all_controllables = dict()

        for item in self.model.get_category_config("controllables"):
            con_instance = self.all_connections[item["con_id"]]
            con_params = item["con_params"]
            metadata = {"description": item["description"], "type": item["type"]}

            if item["type"] == "door" or item["type"] == "sunblind":
                self.all_controllables[item["id"]] = get_slider_by_params(con_instance, con_params, metadata)

            elif item["type"] == "lighting" or item["type"] == "fan":
                self.all_controllables[item["id"]] = get_trigger_by_params(con_instance, con_params["sr_pin"], metadata)

    def __resolve_obj_by_id(self, obj_id: str) -> AbsControllable:
        if type(obj_id) != str:
            raise ValueError('Value must be a string literal')

        if obj_id not in self.all_controllables:
            raise ValueError('id not found')

        return self.all_controllables[obj_id]

    def toggle_controllable(self, obj_id: str):
        """
        Функция для переключения объекта в противоположное состояние
        :param obj_id: идентификатор объекта
        :return: True - успешно, False - неуспешно
        """
        obj_alias = self.__resolve_obj_by_id(obj_id)

        obj_alias.toggle()

        return True

    def get_permitted_actions(self, obj_id: str) -> list:  # Fixme: TD3
        obj_alias = self.__resolve_obj_by_id(obj_id)

        if isinstance(obj_alias, AbsSlider):
            return ["open", "close", "toggle"]
        elif isinstance(obj_alias, AbsTrigger):
            return ["on", "off", "toggle"]
        elif isinstance(obj_alias, AbsControllable):
            return ["toggle"]
        else:
            raise RuntimeError("Resolved object is not controllable: {0}".format(obj_alias))

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
        if action == "print":
            self.print_obj_info(obj_id)
            return

        self.check_action_permitted(obj_id, action, action_params)

        obj_alias = self.__resolve_obj_by_id(obj_id)

        try:
            method_to_call = getattr(obj_alias, action)
            method_to_call(*action_params)
        except AttributeError:
            raise

    def __get_resolved_object_info(self, obj_id: str, obj: AbsControllable) -> dict:  # Fixme: CC13
        """
        Извлечь инфрмацию об объекте
        :param obj_id: ID объекта
        :param obj: ссылка на объект
        :return: словарь с информацией об объекте
        """
        obj_info = dict()  # Создаем новый словарь
        obj_info["id"] = obj_id  # Записываем ID в словарь
        obj_info["status"] = obj.get_state_string()  # Записываем текущее состояние в словарь
        obj_info["actions"] = self.get_permitted_actions(obj_id)  # Записываем действия, доступные пользователю
        obj_info.update(obj.get_metadata())  # Записываем метаданные

        return obj_info

    def get_object_info(self, obj_id: str) -> dict:  # Fixme: TD3, CC13
        """
        Получить информацию об объекте по ID.
        :param obj_id: ID объекта
        :return: словарь в формате:
        {
            "id": "D1",
            "type": "door",
            "actions": ["open", "close", "toggle"],
            "description": "Entrance door",
            "status": "opened"
        }
        """
        obj = self.__resolve_obj_by_id(obj_id)  # Получаем объект по ID
        return self.__get_resolved_object_info(obj_id, obj)

    def get_all_objects_info(self) -> list:  # Fixme: CC13
        """
        Получить информацию о всех объектах в системе
        :return: список с информацией обо всех объектах
        """
        info_list = list()

        for obj_id, obj in self.all_controllables.items():
            info_list.append(self.__get_resolved_object_info(obj_id, obj))

        return info_list

    def print_obj_info(self, obj_id: str):
        print(self.get_object_info(obj_id))
