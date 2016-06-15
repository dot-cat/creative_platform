import serial
from control_objects.control_objects import ControlObjects
from threading import Thread, Event
# from .listener import Listener


class ListenerCli(object):
    def __init__(self, controlling):
        """
        Конструктор. Запускает процесс-слушатель в консоли
        """
        # Listener.__init__(self)

        if type(controlling) != ControlObjects:
            raise ValueError('wrong type of controllable object')

        self.stop_event = Event()

        self.controlling = controlling
        self.listener_thread = Thread(target=self.__data_waiter, daemon=True)
        self.listener_thread.start()

    def __del__(self):
        """
        Деструктор. Останавливает процессы
        :return: None
        """
        self.stop_event.set()

    def __data_waiter(self):
        """
        Слушатель. Ждет строки-команды в консоли и запускает ее обработчик
        :return: None
        """
        while not self.stop_event.is_set():
            data = input()
            thread = Thread(target=self.__handler, args=(data,), daemon=True)
            thread.start()  # запускаем дочерний поток

    def __handler(self, event):
        """
        Обработчик событий
        :param event: событие, строка
        :return: None
        """
        print('event: {0}'.format(event))

        if   event[0:11] == 'toggle door':
            print(event[12:])
            self.controlling.toggle_door(event[12:])

        elif event[0:12] == 'toggle light':
            print(event[13:])
            self.controlling.toggle_light(event[13:])

        elif event[0:13] == 'toggle cooler':
            print(event[14:])
            self.controlling.toggle_cooler(event[14:])

        elif event[0:12] == 'toggle blind':
            print(event[13:])
            self.controlling.toggle_blind(event[13:])

        else:
            print('Warning: Unknown command: {0}'.format(event))

        print('command executed')
