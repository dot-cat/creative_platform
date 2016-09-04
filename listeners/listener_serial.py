import logging
import serial

from listeners.listener import Listener
from controllable_objects.control_objects import ControlObjects


class ListenerSerial(Listener):
    def __init__(self, feedback, tty, baudrate):
        """
        Конструктор. Запускает процесс-слушатель на порту tty
        :param feedback: объект управления
        :param tty: UART-устройство
        :param baudrate: скорость порта
        """
        if not isinstance(feedback, ControlObjects):
            raise ValueError('wrong type of controllable object')

        if type(tty) != str:
            raise ValueError('tty must be a string')

        if type(baudrate) != int or baudrate <= 0:
            raise ValueError('baud-rate value must be positive')

        self.serial = serial.Serial(tty)
        self.serial.baudrate = baudrate

        super().__init__(feedback)

        # another test here

    def __del__(self):
        """
        Деструктор. Освобождает занятые порты, останавливает процессы
        :return: None
        """

        # FIXME: Зачем эта строка?
        super().__del__()

    def get_data(self):
        """
        Считываем очередную строку из tty-устройства
        :return: считанная строка
        """
        return self.serial.readline()

    def process_data(self, raw_data):
        """
        Обработчик считанных данных
        :param raw_data: данные, строка
        :return: None
        """
        logging.debug('Data read: {0}'.format(raw_data))

        if   raw_data == b'B1\r\n':
            self.feedback.toggle_controllable("D3")

        elif raw_data == b'B2\r\n':
            self.feedback.toggle_controllable("D2")

        elif raw_data == b'B3\r\n':
            self.feedback.toggle_controllable("D3")

        elif raw_data == b'B4\r\n':
            self.feedback.toggle_controllable("D2")

        elif raw_data == b'B5\r\n':
            self.feedback.toggle_controllable("SB2")

        elif raw_data == b'B6\r\n':
            self.feedback.toggle_controllable("SB4")

        elif raw_data == b'B8\r\n':
            self.feedback.toggle_controllable("D1")

        else:
            print('Warning: Unknown message: {0}'.format(raw_data))
