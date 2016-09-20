import os.path
import logging

from listeners.listener_serial import ListenerSerial
from listeners.listener_cli import ListenerCli
from events.event_hub import EventHub


class ControllerListeners(object):
    def __init__(self, event_hub: EventHub):
        self.event_hub = event_hub

        self.__start_all_listeners()

    def __start_all_listeners(self):
        self.listener_serial = self.__start_serial_listener('/dev/main_ard_tty', 9600)

        self.listener_cli = ListenerCli(self.event_hub)
        self.listener_cli.start()

    def __start_serial_listener(self, device, speed):
        """
        Инициализация и запуск слушателя последовательного интерфейса
        :param device: tty-устройство
        :param speed: скорость соединения
        :return: Обьект типа ListenerSerial в случае удачи, None - в случае ошибки
        """
        listener_serial = None  # Устанавливаем возращаемое значение по умолчанию

        if os.path.exists(device):  # Если путь к устройству верный...
            listener_serial = ListenerSerial(self.event_hub, device, speed)  # ...иницализируем слушателя
            listener_serial.start()  # ...запускаем слушателя

        else:  # Иначе...
            logging.warning("Unable to open specified serial device: {0}. "
                            "ListenerSerial disabled".format(device))

        return listener_serial
