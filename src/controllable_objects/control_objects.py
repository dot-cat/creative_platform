from connections.shift_reg_buffered import ShiftRegBuffered
from connections.shift_reg_gpio import ShiftRegGPIO

from controllable_objects.factories.slider_factory import get_slider_by_params
from controllable_objects.factories.trigger_factory import get_trigger_by_params

from model import Model

import logging


##############################################################################################
# FIXME List:
# CC7 - Consider Change 7
#   Метод do_action() ничего не возвращает. Возможно, следует этот факт изменить. Варианты:
#   * выкидывать наружу возращаемое значение вызванного метода;
#   * возвращать 0 при успехе и другие значения при ошибке;
#   * оставить как есть, ничего не возвращать, выбрасывать исключения в случае ошибки.
# CC8 - Consider Change 8
#   Сейчас действия выполняются только над controllable'ами. Может разрешить выполнение
#   действий и над другими объектами? Но тогда нужно реализовать TD2
# TD1 - To Do 1
#   Сделать полноценную реализацию метода do_action.
# TD2 - To Do 2
#   Сделать полноценную реализацию проверки разрешений на выполнение действия.
##############################################################################################


class ControlObjects(object):

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, необходимых для вывода
        :return: none
        """
        logging.debug("{0} init started".format(self))

        model_ins = Model("./configs")

        model_data = model_ins.get_config_data()

        # -------------------------------------------------

        self.all_connections = dict()

        con_data_list = model_data["connections"]

        for item in con_data_list:
            if item["con_type"] == "shiftreg":
                self.all_connections[item["id"]] = \
                    ShiftRegBuffered(
                        ShiftRegGPIO(**item["con_params"])
                    )

        # -------------------------------------------------

        self.all_controllables = dict()

        for item in model_data["controllables"]:
            con_instance = self.all_connections[item["con_id"]]
            con_params = item["con_params"]

            if item["type"] == "door" or item["type"] == "sunblind":
                self.all_controllables[item["id"]] = get_slider_by_params(con_instance, con_params)

            elif item["type"] == "lighting" or item["type"] == "fan":
                self.all_controllables[item["id"]] = get_trigger_by_params(con_instance, con_params["sr_pin"])

        # -------------------------------------------------

        logging.debug("{0} init finished".format(self))

    def __del__(self):
        """
        Деструктор, производит установку всех компонентов в начальное состояние
        :return: none
        """
        logging.debug("{0} destruction started".format(self))

        self.all_controllables.clear()
        self.all_connections.clear()

        logging.debug("{0} destruction finished".format(self))
        return

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
        logging.WARNING("Permission checking is not implemented")
        pass

    def do_action(self, obj_id: str, action: str, action_params=None):
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
            method_to_call(action_params)
        except AttributeError:
            raise
