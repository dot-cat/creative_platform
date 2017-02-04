import logging
import os.path

from dpl.listeners.listener_cli import ListenerCli
from dpl.listeners.listener_serial import ListenerSerial
from dpl.messages.message_hub import MessageHub


class ControllerListeners(object):
    def __init__(self, msg_hub: MessageHub):
        self.msg_hub = msg_hub

        self.__start_all_listeners()

    def __start_all_listeners(self):
        self.listener_serial = self.__start_serial_listener('/dev/main_ard_tty', 9600)

        self.listener_cli = ListenerCli(self.msg_hub)
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
            # ...иницализируем слушателя
            listener_serial = ListenerSerial(self.msg_hub, device, speed)
            listener_serial.start()  # ...запускаем слушателя

        else:  # Иначе...
            logging.warning("Unable to open specified serial device: %s. "
                            "ListenerSerial disabled", device)

        return listener_serial
