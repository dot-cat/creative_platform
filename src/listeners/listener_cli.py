import logging

from listeners.listener import Listener
from events.event_hub import EventHub
from events.abs_message import Message, time


class ListenerCli(Listener):
    def __init__(self, feedback):
        """
        Конструктор. Запускает процесс-слушатель консоли
        """
        if not isinstance(feedback, EventHub):
            raise ValueError('wrong type of feedback object')

        super().__init__(feedback)

    def get_data(self):
        """
        Считываем очередную строку из консоли
        :return: считанная строка
        """
        return input()

    def process_data(self, raw_data: str):
        """
        Обработчик считанных данных
        :param raw_data: данные, строка
        :return: None
        """
        logging.debug('Data read: {0}'.format(raw_data))

        tokenized_data = raw_data.split(" ", maxsplit=3)

        if len(tokenized_data) < 2:
            print('Warning: Unknown command: {0}'.format(raw_data))
            return

        command = tokenized_data[0]
        obj_id = tokenized_data[1]

        if len(tokenized_data) > 2:
            cmd_params = tokenized_data[2]
        else:
            cmd_params = tuple()

        msg = Message(
            "user_request",
            "cli",
            "action_requested",
            time.time(),
            {
                "obj_id": obj_id,
                "action": command,
                "action_params": cmd_params
            }
        )

        self.feedback.accept_event(msg)

        print('command "{0}" executed'.format(raw_data))
