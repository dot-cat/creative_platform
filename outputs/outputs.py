import RPi.GPIO as GPIO
import time



class Outputs(object):
    # Константы:
    ON  = True
    OFF = False
    ACTIONS = [ON, OFF]
    ROOMS = ['name', 'name2']

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, нееобходимых для вывода
        :return: none
        """
        # TODO: написать код и убрать NotImplementedError
        raise NotImplementedError('Not implemented')
        return

    def __del__(self):
        """
        Деструктор, проивзодит установку всех компонентов в начальное состояние
        :return: none
        """
        # TODO: пока БЕЗ cleanup!!!!
        return

    def open_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        # TODO: написать код и убрать NotImplementedError
        raise NotImplementedError('Not implemented')
        return False

    def turn_light(self, room_name, light_action):
        """
        Включение или выключение света
        :param room_name: имя комнаты, строка
        :param light_action: включить либо выключить свет
        :return: True - успешно, False - неуспешно
        """
        if type(room_name) != str:
            raise ValueError('room_name must be a string')

        elif room_name not in self.ROOMS:
            raise ValueError('unable to find the room with such name')

        elif light_action not in self.ACTIONS:
            raise ValueError('wrong action with lights')


        # TODO: написать код и убрать NotImplementedError


        raise NotImplementedError('Not implemented')
        return False