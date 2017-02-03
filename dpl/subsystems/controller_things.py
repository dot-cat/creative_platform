##############################################################################################
# FIXME List:
# TD3 - To Do 3
#   Переписать метод get_permitted_actions, добавить проверку пользователя, обработку
#   дополнительных условий.
# CC7 - Consider Change 7
#   Метод do_action() ничего не возвращает. Возможно, следует этот факт изменить. Варианты:
#   * выкидывать наружу возращаемое значение вызванного метода;
#   * возвращать 0 при успехе и другие значения при ошибке;
#   * оставить как есть, ничего не возвращать, выбрасывать исключения в случае ошибки.
# CC13 - Consider Change 13
#   Кешировать информацию об объектах.
##############################################################################################

import logging

from dpl.core.config import Config
from dpl.core.connections import get_connection_by_config
from dpl.core.things import Player
from dpl.core.things import Slider
from dpl.core.things import Thing
from dpl.core.things import Trigger
from dpl.core.things import get_thing_by_params

# noinspection PyUnresolvedReferences
import dpl.specific.connections

# noinspection PyUnresolvedReferences
import dpl.specific.things


class ControllerThings(object):
    def __init__(self, model: Config):
        self.model = model

        self.__init_all_connections()
        self.__init_all_things()

    def __del__(self):
        self.all_things.clear()
        self.all_connections.clear()

    def __init_all_connections(self):
        self.all_connections = dict()

        con_data_list = self.model.get_category_config("connections")

        for item in con_data_list:
            new_conn = get_connection_by_config(item)

            if new_conn is not None:
                self.all_connections[item["id"]] = new_conn

    def __init_all_things(self):
        self.all_things = dict()

        for item in self.model.get_category_config("things"):
            item_id = item["id"]
            con_id = item["con_id"]

            con_instance = self.all_connections.get(con_id, None)
            if con_instance is None:
                logging.warning(
                    "Unable to init component: %s. "
                    "Connection %s is unavailable",
                    item_id, con_id
                )
                continue

            metadata = {"description": item["description"], "type": item["type"]}

            new_object = get_thing_by_params(con_instance, item["con_params"], metadata)

            if new_object is not None:
                self.all_things[item_id] = new_object

    def __resolve_obj_by_id(self, obj_id: str) -> Thing:
        if not isinstance(obj_id, str):
            raise ValueError('Value must be a string literal')

        if obj_id not in self.all_things:
            raise ValueError('id not found')

        return self.all_things[obj_id]

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

        if isinstance(obj_alias, Slider):
            return ["open", "close", "toggle"]
        elif isinstance(obj_alias, Trigger):
            return ["on", "off", "toggle"]
        elif isinstance(obj_alias, Player):
            return ["play", "stop", "pause", "toggle", "prev", "next"]
        elif isinstance(obj_alias, Thing):
            return ["toggle"]
        else:
            raise RuntimeError("Resolved object is not a thing: {0}".format(obj_alias))

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
        :return: Результат выполнения действия на объекте. Может быть None  # CC7
        """
        # FIXME: TD1
        if action == "print":
            self.print_obj_info(obj_id)
            return

        self.check_action_permitted(obj_id, action, action_params)

        obj_alias = self.__resolve_obj_by_id(obj_id)

        try:
            method_to_call = getattr(obj_alias, action)
            return method_to_call(*action_params)
        except AttributeError:
            raise

    def __get_resolved_object_info(self, obj_id: str, obj: Thing) -> dict:  # Fixme: CC13
        """
        Извлечь инфрмацию об объекте
        :param obj_id: ID объекта
        :param obj: ссылка на объект
        :return: словарь с информацией об объекте
        """
        # Создаем новый словарь
        obj_info = dict()

        # Заполняем его значениями
        obj_info["id"] = obj_id  # ID объекта
        obj_info["status"] = obj.get_state_string()  # текущее состояние
        obj_info["actions"] = self.get_permitted_actions(obj_id)  # действия, доступные пользователю
        obj_info.update(obj.get_metadata())  # метаданные

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

        for obj_id, obj in self.all_things.items():
            info_list.append(self.__get_resolved_object_info(obj_id, obj))

        return info_list

    def print_obj_info(self, obj_id: str):
        print(self.get_object_info(obj_id))
