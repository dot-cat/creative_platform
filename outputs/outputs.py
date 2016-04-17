import RPi.GPIO as GPIO
import time

from shift_reg_lib import ShiftRegister


# устанавливаем пины
si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

WorkRegistr = ShiftRegister(si, sck, rck, sclr)


class PinData(object):
    def __init__(self, pin_number, value):
        self.pin_number = pin_number
        self.value = value
        return 
    

class Outputs(object):
    # Константы:
    ON  = True
    OFF = False
    ACTIONS = [ON, OFF]

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, нееобходимых для вывода
        :return: none
        """

        self.door_1_plus  = 0
        self.door_1_minus = 1
        self.door_2_plus  = 2
        self.door_2_minus = 3
        self.diode_1 = 4
        self.diode_2 = 5
        self.door_3_plus  = 6
        self.door_3_minus = 7
        self.door_4_plus  = 8
        self.door_4_minus = 9
        self.diode_3 = 10
        self.diode_4 = 11
        self.blind_1_plus  = 12
        self.blind_1_minus = 13
        self.blind_2_plus  = 14
        self.blind_2_minus = 15
        self.blind_3_plus  = 16
        self.blind_3_minus = 17
        self.diode_5 = 18
        self.diode_6 = 19
        self.cooler  = 20

        self.current_state = 0x0

        self.control_Door_dict = {'Open first door':   [PinData(self.door_1_plus, 1), PinData(self.door_1_minus, 0)],
                                  'Close first door':  [PinData(self.door_1_plus, 0), PinData(self.door_1_minus, 1)],
                                  'Open second door':  [PinData(self.door_2_plus, 1), PinData(self.door_2_minus, 0)],
                                  'Close second door': [PinData(self.door_2_plus, 0), PinData(self.door_2_minus, 1)],
                                  'Open third door':   [PinData(self.door_3_plus, 1), PinData(self.door_3_minus, 0)],
                                  'Close third door':  [PinData(self.door_3_plus, 0), PinData(self.door_3_minus, 1)],
                                  'Open fourth door':  [PinData(self.door_4_plus, 1), PinData(self.door_4_minus, 0)],
                                  'Close fourth door': [PinData(self.door_4_plus, 0), PinData(self.door_4_minus, 1)]
                                  }

        self.room_led_dict = {'room 1':  self.diode_1,
                              'room 2':  self.diode_2,
                              'room 3':  self.diode_3,
                              'room 4':  self.diode_4,
                              'room 5':  self.diode_5,
                              'room 6':  self.diode_6
                              }

        self.control_Cooler_dict = {'On cooler':  PinData(self.cooler, 1),
                                    'Off cooler': PinData(self.cooler, 0)}

        self.control_Blind_dict = {'Open first blind':   [PinData(self.blind_1_plus, 1), PinData(self.blind_1_minus, 0)],
                                   'Close first blind':  [PinData(self.blind_1_plus, 0), PinData(self.blind_1_minus, 1)],
                                   'Open second blind':  [PinData(self.blind_2_plus, 1), PinData(self.blind_1_minus, 0)],
                                   'Close second blind': [PinData(self.blind_2_plus, 0), PinData(self.blind_1_minus, 1)],
                                   'Open third blind':   [PinData(self.blind_3_plus, 1), PinData(self.blind_1_minus, 0)],
                                   'Close third blind':  [PinData(self.blind_3_plus, 0), PinData(self.blind_1_minus, 1)]
                                   }


        return

    def __del__(self):
        """
        Деструктор, проивзодит установку всех компонентов в начальное состояние
        :return: none
        """
        self.control_Door_dict.clear()
        self.room_led_dict.clear()
        self.control_Cooler_dict.clear()
        self.control_Blind_dict.clear()
        return

    def open_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.control_Door_dict:
            raise ValueError('Value not found')

        door_data = self.control_Door_dict.get(door_id)
        if(self.check_bit(door_data[0].pin_number) == 1):
            self.set_bit(door_data[0].pin_number, self.ON)
            self.set_bit(door_data[1].pin_number, self.ON)
            WorkRegistr.write_data(self.current_state)
            return
        else:
            self.set_bit(door_data[0].pin_number, door_data[0].value)
            self.set_bit(door_data[1].pin_number, door_data[1].value)
            WorkRegistr.write_data(self.current_state)
            return True

    def close_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.control_Door_dict:
            raise ValueError('Value not found')

        door_data = self.control_Door_dict.get(door_id)
        if (self.check_bit(door_data[0].pin_number) == 0):
            self.set_bit(door_data[0].pin_number, self.OFF)
            self.set_bit(door_data[1].pin_number, self.OFF)
            WorkRegistr.write_data(self.current_state)
            return
        else:
            self.set_bit(door_data[0].pin_number, door_data[0].value)
            self.set_bit(door_data[1].pin_number, door_data[1].value)
            WorkRegistr.write_data(self.current_state)
            return True


    def stop_door(self, door_id):
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.control_Door_dict:
            raise ValueError('Value not found')

        door_data = self.control_Door_dict.get(door_id)
        if (self.check_bit(door_data[0].pin_number) == 0):
            self.set_bit(door_data[0].pin_number, self.OFF)
            self.set_bit(door_data[1].pin_number, self.OFF)
            WorkRegistr.write_data(self.current_state)
            return
        else:
            self.set_bit(door_data[0].pin_number, self.ON)
            self.set_bit(door_data[1].pin_number, self.ON)
            WorkRegistr.write_data(self.current_state)



    def turn_light(self, room_name, light_action):
        """
        Включение или выключение света
        :param room_name: имя комнаты, строка
        :param light_action: включить либо выключить свет
        :return: True - успешно, False - неуспешно
        """
        if type(room_name) != str:
            raise ValueError('room_name must be a string')

        elif room_name not in self.room_led_dict:
            raise ValueError('unable to find the room with such name')

        elif light_action not in self.ACTIONS:
            raise ValueError('wrong action with lights')

        elif room_name not in self.room_led_dict:
            raise ValueError('Value not found')

        led_data = self.room_led_dict.get(room_name)

        if light_action == self.ON:
            self.set_bit(led_data, 1)

        elif light_action == self.OFF:
            self.set_bit(led_data, 0)

        else:
            raise ValueError('Unknown action')

        WorkRegistr.write_data(self.current_state)

        return True

    def set_bit(self, bit_num, value):
        if bit_num < 0:
            raise ValueError('Bit number must be positive or zero')

        if value != 0 and value != 1:
            raise ValueError('Value must be 1 or zero, True or False')

        if value == 0:
            self.current_state &= ~(1 << bit_num)

        else:
            self.current_state |= (1 << bit_num)

        return


    def check_bit(self, bit_num):
        if bit_num < 0:
            raise ValueError('Bit number must be positive or zero')
        copy_current_state = self.current_state

        if ((copy_current_state >> bit_num) & 1):
            return 1
        else:
            return 0






