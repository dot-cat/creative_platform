import logging
import serial

from listeners.listener import Listener
from controllable_objects.control_objects import ControlObjects


class ListenerSerial(Listener):
    def __init__(self, feedback, con_instance: serial.Serial, con_params=None):
        """
        Конструктор. Запускает процесс-слушатель на порту tty
        :param feedback: объект управления
        :param con_instance: объект-подключение типа serial.Serial
        :param con_params: настройки доступа к подключению, не используется
        """
        if not isinstance(feedback, ControlObjects):
            raise ValueError('wrong type of controllable object')

        if not isinstance(con_instance, serial.Serial):
            raise ValueError('con_instance must be an instance of serial.Serial type')

        super().__init__(feedback, con_instance, con_params)

    def get_data(self):
        """
        Считываем очередную строку из tty-устройства
        :return: считанная строка
        """
        return self.con_instance.readline()

    def process_data(self, raw_data):
        """
        Обработчик считанных данных
        :param raw_data: данные, строка
        :return: None
        """
        logging.debug('Data read: {0}'.format(raw_data))

        if   raw_data == b'B1\r\n':
            self.feedback.toggle_door('Office door')

        elif raw_data == b'B2\r\n':
            self.feedback.toggle_door('Bedroom door')

        elif raw_data == b'B3\r\n':
            self.feedback.toggle_door('Office door')

        elif raw_data == b'B4\r\n':
            self.feedback.toggle_door('Bedroom door')

        elif raw_data == b'B5\r\n':
            self.feedback.toggle_blind('Bedroom')

        elif raw_data == b'B6\r\n':
            self.feedback.toggle_blind('Living Room')

        elif raw_data == b'B8\r\n':
            self.feedback.toggle_door('Entrance door')

        else:
            print('Warning: Unknown message: {0}'.format(raw_data))
