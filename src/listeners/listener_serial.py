import logging
import serial

from listeners.listener import Listener
from messages.abs_message import Message, time
from messages.message_hub import MessageHub


class ListenerSerial(Listener):
    def __init__(self, feedback, tty, baudrate):
        """
        Конструктор. Запускает процесс-слушатель на порту tty
        :param feedback: объект управления
        :param tty: UART-устройство
        :param baudrate: скорость порта
        """
        if not isinstance(feedback, MessageHub):
            raise ValueError('wrong type of feedback object')

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

    def process_data(self, raw_data: bytes):
        """
        Обработчик считанных данных
        :param raw_data: данные, строка
        :return: None
        """
        id = raw_data.strip(b"\r\n").decode()
        if id[0] == "B":
            logging.debug('Data read: {0}'.format(raw_data))
            msg = Message("button", id, "pressed", time.time(), None)
            self.feedback.accept_msg(msg)

