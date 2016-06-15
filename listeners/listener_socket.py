import serial
from control_objects.control_objects import ControlObjects
from threading import Thread, Event
# from .listener import Listener


class ListenerSocket(object):
    def __init__(self):
        """
        Конструктор. Запускает процесс-слушатель на сокете
        """
        # Listener.__init__(self)
        pass

    def __del__(self):
        """
        Деструктор. Освобождает занятые порты, останавливает процессы
        :return: None
        """
        pass

    def __data_waiter(self):
        """
        Слушатель. Ждет сообщения на сокете и запускает его обработчик
        :return: None
        """
        pass

    def __handler(self, event):
        """
        Обработчик событий
        :param event: событие, строка
        :return: None
        """
        pass
