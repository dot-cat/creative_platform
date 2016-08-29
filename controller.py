import RPi.GPIO as GPIO
import logging
import os.path

from controllable_objects.control_objects import ControlObjects
from listeners.listener_serial import ListenerSerial
from listeners.listener_cli import ListenerCli
import utils.debug_refs as debug_refs


class Controller(object):
    def start_serial_listener(self, device, speed):
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

    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        logging.debug("{0} init started".format(self))

        self.to_control = ControlObjects()

        self.listener_serial = self.start_serial_listener('/dev/main_ard_tty', 9600)

        self.listener_cli = ListenerCli(self.to_control)
        self.listener_cli.start()

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

        # Fixme: Consider deletion of the bottom line
        GPIO.cleanup()  # Освобождаем порты GPIO

        logging.debug("{0} destruction finished".format(self))

        pass
