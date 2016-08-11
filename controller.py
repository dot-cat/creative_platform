import RPi.GPIO as GPIO
import logging

from control_objects.control_objects import ControlObjects
from listeners.listener_serial import ListenerSerial
from listeners.listener_cli import ListenerCli
import utils.debug_refs as debug_refs


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        logging.debug("{0} init started".format(self))

        self.to_control = ControlObjects()
        self.listener_serial = ListenerSerial(self.to_control, '/dev/main_ard_tty', 9600)
        self.listener_cli = ListenerCli(self.to_control)

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

        logging.debug("{0} destruction finished".format(self))

        pass
