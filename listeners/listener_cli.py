import logging

from listeners.listener import Listener
from controllable_objects.control_objects import ControlObjects


class ListenerCli(Listener):
    def __init__(self, feedback):
        """
        Конструктор. Запускает процесс-слушатель консоли
        """
        if not isinstance(feedback, ControlObjects):
            raise ValueError('wrong type of controllable object')

        super().__init__(feedback)

    def get_data(self):
        """
        Считываем очередную строку из консоли
        :return: считанная строка
        """
        return input()

    def process_data(self, raw_data):
        """
        Обработчик считанных данных
        :param raw_data: данные, строка
        :return: None
        """
        logging.debug('Data read: {0}'.format(raw_data))

        if raw_data[0:11] == 'toggle door':
            logging.debug(raw_data[12:])
            self.feedback.toggle_controllable(raw_data[12:])

        elif raw_data[0:12] == 'toggle light':
            logging.debug(raw_data[13:])
            self.feedback.toggle_light(raw_data[13:])

        elif raw_data[0:13] == 'toggle cooler':
            logging.debug(raw_data[14:])
            self.feedback.toggle_cooler(raw_data[14:])

        elif raw_data[0:12] == 'toggle blind':
            logging.debug(raw_data[13:])
            self.feedback.toggle_blind(raw_data[13:])

        else:
            print('Warning: Unknown command: {0}'.format(raw_data))

        print('command "{0}" executed'.format(raw_data))
