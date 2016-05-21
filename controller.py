from outputs.outputs import Outputs
from actors.actor_serial import ActorSerial
import RPi.GPIO as GPIO


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        self.outputs = Outputs()
        self.actor_serial = ActorSerial(self.outputs, '/dev/main_ard_tty', 9600)

    def __del__(self):
        """
        Конструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        pass