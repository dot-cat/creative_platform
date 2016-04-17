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


        self.openfirstdoor = 0x2 #равносильно 0b10
        self.closefirstdoor = 0x1#равносильно 0b01

        self.openseconddoor = 0x8
        self.closeseconddoor = 0x4

        self.openthirddoor = 0x80
        self.closethirddoor = 0x40

        self.openfourthdoor = 0x200
        self.closefourthdoor = 0x100



        self.firstLED = 0x10
        self.secondLED = 0x20
        self.thirdLED = 0x400
        self.fourthLED = 0x800
        self.fifthLED = 0x40000
        self.sixthLED = 0x80000


        self.cooler = 0x200000


        self.openfirstblind = 0x2000
        self.closefirstblind = 0x1000

        self.opensecondblind = 0x8000
        self.closesecondblind = 0x4000

        self.openthirdblind = 0x20000
        self.closethirdblind = 0x10000
        return

    def __del__(self):
        """
        Деструктор, проивзодит установку всех компонентов в начальное состояние
        :return: none
        """


        # TODO: пока БЕЗ cleanup!!!!
        return
    open_door('to kitchen')
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