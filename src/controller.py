import logging
import os.path

import RPi.GPIO as GPIO

import utils.debug_refs as debug_refs
from controllable_objects.control_objects import ControlObjects
from listeners.listener_cli import ListenerCli
from listeners.listener_serial import ListenerSerial


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        logging.debug("{0} init started".format(self))

        self.__init_all_controllables()

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
        debug_refs.print_referrers(self.to_control)

        del self.listener_serial
        del self.listener_cli
        del self.to_control

        logging.debug("{0} destruction finished".format(self))

        pass

    def __start_all_listeners(self):
        self.listener_serial = self.__start_serial_listener('/dev/main_ard_tty', 9600)

        self.listener_cli = ListenerCli(self.to_control)
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
            listener_serial = ListenerSerial(self.to_control, device, speed)  # ...иницализируем слушателя
            listener_serial.start()  # ...запускаем слушателя

        else:  # Иначе...
            logging.warning("Unable to open specified serial device: {0}. "
                            "ListenerSerial disabled".format(device))

        return listener_serial

    def __init_all_controllables(self):
        self.to_control = ControlObjects()
