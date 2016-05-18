import serial
from outputs.outputs import Outputs
from threading import Thread, Event


class ActorSerial(object):
    def __init__(self, controlling, tty, baudrate):
        """
        Конструктор. Запускает процесс-слушатель на порту tty
        :param controlling: объект управления
        :param tty: UART-устройство
        :param baudrate: скорость порта
        """
        if type(controlling) != Outputs:
            raise ValueError('wrong type of controllable object')

        if type(tty) != str:
            raise ValueError('tty must be a string')

        if type(baudrate) != int or baudrate <= 0:
            raise ValueError('baud-rate value must be positive')

        self.stop_event = Event()
        self.serial = serial.Serial(tty)
        self.serial.baudrate = baudrate
        self.controlling = controlling
        self.listener_thread = Thread(target=self._listener, daemon=True)
        self.listener_thread.start()

    def __del__(self):
        """
        Деструктор. Освобождает занятые порты, останавливает процессы
        :return: None
        """
        self.stop_event.set()
        self.serial.close()

    def _listener(self):
        """
        Слушатель. Ждет события в консоли и запускает его обработчик
        :return: None
        """
        while not self.stop_event.is_set():
            data = self.serial.readline()
            thread = Thread(target=self._handler, args=(data,), daemon=True)
            thread.start()  # запускаем дочерний поток

    def _handler(self, event):
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

        else:
            print('Warning: Unknown event: {0}'.format(event))
