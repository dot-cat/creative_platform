from controllable_objects.specific.shift_reg.slider import Slider as SRSlider
from controllable_objects.specific.shift_reg.trigger import Trigger as SRTrigger

from connections.shift_reg_wrapper import ShiftRegWrapper

from model import Model

import logging


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
                self.all_connections[item["id"]] = ShiftRegWrapper(**item["con_params"])

        # -------------------------------------------------

        self.all_controllables = dict()

        for item in model_data["controllables"]:
            target_connection = self.all_connections[item["con_id"]]

            if isinstance(target_connection, ShiftRegWrapper):
                TriggerType = SRTrigger
                SliderType = SRSlider
            else:
                logging.warning("Unknown {0} item connection type: {1}. Ignoring".format(
                    item["id"], type(target_connection)
                ))
                continue

            con_params = item["con_params"]

            if item["type"] == "door" or item["type"] == "sunblind":
                self.all_controllables[item["id"]] = SliderType(
                    target_connection,
                    SRSlider.ConParams(con_params["pin_pos"], con_params["pin_neg"]),
                    con_params["transition_time"]
                )
            elif item["type"] == "lighting" or item["type"] == "fan":
                self.all_controllables[item["id"]] = TriggerType(target_connection, con_params["sr_pin"])

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

    def toggle_controllable(self, obj_id):
        """
        Функция для переключения объекта в противоположное состояние
        :param obj_id: идентификатор объекта
        :return: True - успешно, False - неуспешно
        """
        if type(obj_id) != str:
            raise ValueError('Value must be a string literal')

        if obj_id not in self.all_controllables:
            raise ValueError('id not found')

        obj_alias = self.all_controllables[obj_id]

        obj_alias.toggle()

        return True
