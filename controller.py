from control_objects.control_objects import ControlObjects
from listeners.listener_serial import ListenerSerial
import RPi.GPIO as GPIO


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        self.to_control = ControlObjects()
        self.listener_serial = ListenerSerial(self.to_control, '/dev/main_ard_tty', 9600)

    def __del__(self):
        """
        Деструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        pass
