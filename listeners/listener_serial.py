import serial
from threading import Thread, Event
import logging
import weakref

from control_objects.control_objects import ControlObjects
# from .listener import Listener


class ListenerSerial(object):
    def __init__(self, controlling, tty, baudrate):
        """
        Конструктор. Запускает процесс-слушатель на порту tty
        :param controlling: объект управления
        :param tty: UART-устройство
        :param baudrate: скорость порта
        """
        logging.debug("{0} init started".format(self))

        # Listener.__init__(self)

        if not isinstance(controlling, ControlObjects):
            raise ValueError('wrong type of controllable object')

        if type(tty) != str:
            raise ValueError('tty must be a string')

        if type(baudrate) != int or baudrate <= 0:
            raise ValueError('baud-rate value must be positive')

        # Не удерживаем обьекты контроля от удаления - используем "слабую ссылку"
        self.controlling = weakref.proxy(controlling)

        self.stop_event = Event()
        self.serial = serial.Serial(tty)
        self.serial.baudrate = baudrate
        self.listener_thread = Thread(target=self.__data_waiter, daemon=True)
        self.listener_thread.start()

        logging.debug("{0} init finished".format(self))

    def __del__(self):
        """
        Деструктор. Освобождает занятые порты, останавливает процессы
        :return: None
        """
        logging.debug("{0} destruction started".format(self))

        self.stop_event.set()
        self.serial.close()

        logging.debug("{0} destruction finished".format(self))

    def __data_waiter(self):
        """
        Слушатель. Ждет события в консоли и запускает его обработчик
        :return: None
        """
        while not self.stop_event.is_set():
            data = self.serial.readline()
            thread = Thread(target=self.__handler, args=(data,), daemon=True)
            thread.start()  # запускаем дочерний поток

    def __handler(self, event):
        """
        Обработчик событий
        :param event: событие, строка
        :return: None
        """
        print('event: {0}'.format(event))

        if   event == b'B1\r\n':
            self.controlling.toggle_door('Office door')

        elif event == b'B2\r\n':
            self.controlling.toggle_door('Bedroom door')

        elif event == b'B3\r\n':
            self.controlling.toggle_door('Office door')

        elif event == b'B4\r\n':
            self.controlling.toggle_door('Bedroom door')

        elif event == b'B5\r\n':
            self.controlling.toggle_blind('Bedroom')

        elif event == b'B6\r\n':
            self.controlling.toggle_blind('Living Room')

        elif event == b'B8\r\n':
            self.controlling.toggle_door('Entrance door')

        else:
            print('Warning: Unknown event: {0}'.format(event))
