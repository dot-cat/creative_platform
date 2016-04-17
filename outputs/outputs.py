import RPi.GPIO as GPIO
import time

from shift_reg_lib import ShiftRegister


# устанавливаем пины
si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

WorkRegistr = ShiftRegister(si, sck, rck, sclr)

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

        self.currentstate = 0x0

        self.control_Door_dict = {'Open first door':self.openfirstdoor,
                           'Close first door':self.closefirstdoor,
                            'Open second door': self.openseconddoor,
                            'Close second door': self.closeseconddoor,
                            'Open third door': self.openthirddoor,
                            'Close third door': self.closethirddoor,
                            'Open fourth door': self.openfourthdoor,
                            'Close fourth door': self.closefourthdoor}

        self.controlLED_dict = {'On first LED':self.firstLED,
                                 'Off first LED': self.firstLED,
                                 'On second LED':self.secondLED,
                                 'Off second LED': self.secondLED,
                                 'On third LED': self.thirdLED,
                                 'OFF third LED': self.thirdLED,
                                 'On Fourth LED': self.fourthLED,
                                 'Off Fourth LED': self.fourthLED,
                                 'On fifth LED': self.fifthLED,
                                 'Off fifth LED': self.fifthLED,
                                 'On sixth LED': self.sixthLED,
                                 'Off sixth LED':self.sixthLED}

        self.control_Cooler_dict = {'On cooler': self.cooler,
                                  'Off cooler': self.cooler}


        self.control_Blind_dict = {'Open first blind': self.openfirstblind,
                                 'Close first blind': self.closefirstblind,
                                 'Open second blind': self.opensecondblind,
                                 'Close second blind': self.closesecondblind,
                                 'Open third blind': self.openthirdblind,
                                 'Close third blind': self.closethirdblind}


        return

    def __del__(self):
        """
        Деструктор, проивзодит установку всех компонентов в начальное состояние
        :return: none
        """
        self.control_Door_dict.clear()
        self.controlLED_dict.clear()
        self.control_Cooler_dict.clear()
        self.control_Blind_dict.clear()
        return

    def open_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if door_id != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.control_Door_dict():
            raise ValueError('Value not found')

        RightDoor = self.control_Door_dict.get(door_id)
        WorkRegistr.write_data(RightDoor)


        return

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