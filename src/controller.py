import RPi.GPIO as GPIO
import logging
import os.path

from listeners.listener_serial import ListenerSerial
from listeners.listener_cli import ListenerCli
import utils.debug_refs as debug_refs

from connections.shift_reg_buffered import ShiftRegBuffered
from connections.shift_reg_gpio import ShiftRegGPIO

from controllable_objects.factories.slider_factory import get_slider_by_params
from controllable_objects.factories.trigger_factory import get_trigger_by_params

from model import Model

from events.event_hub import EventHub
from handlers.conf_handler import ConfHandler, HandleConfig, Message, MessagePattern
from handlers.user_request_handler import UserRequestHandler

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
# TD2 - To Do 2
#   Сделать полноценную реализацию проверки разрешений на выполнение действия.
##############################################################################################


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        logging.debug("{0} init started".format(self))

        self.model = Model("./configs")
        self.model_data = self.model.get_config_data()

        self.__init_all_connections()
        self.__init_all_controllables()
        self.__init_handlers()
        self.__init_event_hub()
        self.__start_all_listeners()

        logging.debug("{0} init finished".format(self))

    def __del__(self):
        """
        Деструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        logging.debug("{0} destruction started".format(self))

        debug_refs.print_referrers(self.listener_serial)
        debug_refs.print_referrers(self.listener_cli)

        del self.listener_serial
        del self.listener_cli

        self.all_controllables.clear()
        self.all_connections.clear()

        logging.debug("{0} destruction finished".format(self))

        pass

    def __init_handlers(self):
        self.all_handlers = dict()

        handler_data_list = self.model_data["handlers"]

        for item in handler_data_list:
            id = item["id"]
            pattern = MessagePattern(**item["if"])

            if pattern.type == "user_request":
                self.all_handlers[id] = UserRequestHandler(
                    pattern, self
                )
            else:
                hconfig = HandleConfig()
                hconfig.add_action(**item["then"])
                self.all_handlers[id] = ConfHandler(
                    hconfig, pattern, self
                )

    def __init_event_hub(self):
        self.event_hub = EventHub()

        for handler in self.all_handlers.values():
            self.event_hub.add_handler(handler)

    def __start_all_listeners(self):
        self.listener_serial = self.__start_serial_listener('/dev/ttyUSB0', 9600)

        self.listener_cli = ListenerCli(self.event_hub)
        self.listener_cli.start()

    def __start_serial_listener(self, device, speed):
        """
        Инициализация и запуск слушателя последовательного интерфейса
        :param device: tty-устройство
        :param speed: скорость соединения
        :return: Обьект типа ListenerSerial в случае удачи, None - в случае ошибки
        """
        listener_serial = None  # Устанавливаем возращаемое значение по умолчанию

        if os.path.exists(device):  # Если путь к устройству верный...
            listener_serial = ListenerSerial(self.event_hub, device, speed)  # ...иницализируем слушателя
            listener_serial.start()  # ...запускаем слушателя

        else:  # Иначе...
            logging.warning("Unable to open specified serial device: {0}. "
                            "ListenerSerial disabled".format(device))

        return listener_serial

    def __init_all_connections(self):
        self.all_connections = dict()

        con_data_list = self.model_data["connections"]

        for item in con_data_list:
            if item["con_type"] == "shiftreg":
                self.all_connections[item["id"]] = \
                    ShiftRegBuffered(
                        ShiftRegGPIO(**item["con_params"])
                    )

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
