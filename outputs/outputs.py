import RPi.GPIO as GPIO
import time

from shift_reg_wrapper import ShiftRegWrapper
from control_objects import *


class RotElement(object):
    def __init__(self, shift_plus, shift_minus, rot_time=1):
        self.shift_plus = shift_plus
        self.shift_minus = shift_minus
        self.rot_time = rot_time
        return


class Outputs(object):
    # Константы:
    ON  = True
    OFF = False
    STATES = [ON, OFF]

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, необходимых для вывода
        :return: none
        """
        # устанавливаем пины
        si = 37    # пин для входных данных
        rck = 33   # пин для сдвига регистров хранения
        sck = 35   # пин для синхросигнала и сдвига
        sclr = 40  # пин для очистки

        self.shift_reg = ShiftRegWrapper(si, sck, rck, sclr, 2)

        self.door_1_plus  = 0
        self.door_1_minus = 1
        self.door_2_plus  = 2
        self.door_2_minus = 3
        self.diode_1 = 4
        self.diode_2 = 5
        self.door_3_plus  = 6
        self.door_3_minus = 7
        self.blind_4_plus  = 8
        self.blind_4_minus = 9
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

        self.door_shifts = {
                              'First door':   RotElement(self.door_1_plus, self.door_1_minus),
                              'Second door':  RotElement(self.door_2_plus, self.door_2_minus),
                              'Third door':   RotElement(self.door_3_plus, self.door_3_minus)
                            }

        self.room_led_shifts = {
                                'room 1':  self.diode_1,
                                'room 2':  self.diode_2,
                                'room 3':  self.diode_3,
                                'room 4':  self.diode_4,
                                'room 5':  self.diode_5,
                                'room 6':  self.diode_6
                               }

        self.coolers_shifts = {'cooler':  self.cooler}

        self.blind_shifts = {
                               'First blind':  RotElement(self.blind_1_plus, self.blind_1_minus),
                               'Second blind': RotElement(self.blind_2_plus, self.blind_2_minus),
                               'Third blind':  RotElement(self.blind_3_plus, self.blind_3_minus),
                               'Fourth blind': RotElement(self.blind_4_plus, self.blind_4_minus)
                            }

    def __del__(self):
        """
        Деструктор, проивзодит установку всех компонентов в начальное состояние
        :return: none
        """
        self.door_shifts.clear()
        self.room_led_shifts.clear()
        self.coolers_shifts.clear()
        self.blind_shifts.clear()
        return

    def get_state(self):
        return self.shift_reg.get_buffer()

    def open_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.door_shifts:
            raise ValueError('id not found')

        door_data = self.door_shifts.get(door_id)

        if self.shift_reg.get_buf_bit(door_data.shift_plus) == 1:
            self.shift_reg.set_buf_bit(door_data.shift_plus, 1)
            self.shift_reg.set_buf_bit(door_data.shift_minus, 1)

        else:
            self.shift_reg.set_buf_bit(door_data.shift_plus, 1)
            self.shift_reg.set_buf_bit(door_data.shift_minus, 0)

        self.shift_reg.write_buffer()

        time.sleep(door_data.rot_time)

        self.shift_reg.set_buf_bit(door_data.shift_plus, 1)
        self.shift_reg.set_buf_bit(door_data.shift_minus, 1)

        return True

    def close_door(self, door_id):
        """
        Функция для открытия двери
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.door_shifts:
            raise ValueError('id not found')

        door_data = self.door_shifts.get(door_id)

        if self.shift_reg.get_buf_bit(door_data.shift_plus) == 0:
            self.shift_reg.set_buf_bit(door_data.shift_plus, 0)
            self.shift_reg.set_buf_bit(door_data.shift_minus, 0)

        else:
            self.shift_reg.set_buf_bit(door_data.shift_plus, 0)
            self.shift_reg.set_buf_bit(door_data.shift_minus, 1)

        self.shift_reg.write_buffer()

        time.sleep(door_data.rot_time)

        self.shift_reg.set_buf_bit(door_data.shift_plus, 0)
        self.shift_reg.set_buf_bit(door_data.shift_minus, 0)

        self.shift_reg.write_buffer()

        return True

    def open_blind(self, blind_id):
        """
        Функция для открытия шторы
        :param blind_id: идентификатор шторки
        :return: True - успешно, False - неуспешно
        """
        if type(blind_id) != str:
            raise ValueError('Value must be a string literal')

        if blind_id not in self.blind_shifts:
            raise ValueError('id not found')
        
        blind_data = self.blind_shifts.get(blind_id)

        if self.shift_reg.get_buf_bit(blind_data.shift_plus) == 1:
            self.shift_reg.set_buf_bit(blind_data.shift_plus, 1)
            self.shift_reg.set_buf_bit(blind_data.shift_minus, 1)

        else:
            self.shift_reg.set_buf_bit(blind_data.shift_plus, 1)
            self.shift_reg.set_buf_bit(blind_data.shift_minus, 0)

        self.shift_reg.write_buffer()

        time.sleep(blind_data.rot_time)

        self.shift_reg.set_buf_bit(blind_data.shift_plus, 1)
        self.shift_reg.set_buf_bit(blind_data.shift_minus, 1)

        self.shift_reg.write_buffer()

        return True

    def close_blind(self, blind_id):
        """
        Функция для закрытия шторы
        :param blind_id: идентификатор шторки
        :return: True - успешно, False - неуспешно
        """
        if type(blind_id) != str:
            raise ValueError('Value must be a string literal')

        if blind_id not in self.blind_shifts:
            raise ValueError('id not found')

        blind_data = self.blind_shifts.get(blind_id)

        if self.shift_reg.get_buf_bit(blind_data.shift_plus) == 0:
            self.shift_reg.set_buf_bit(blind_data.shift_plus, 0)
            self.shift_reg.set_buf_bit(blind_data.shift_minus, 0)

        else:
            self.shift_reg.set_buf_bit(blind_data.shift_plus, 0)
            self.shift_reg.set_buf_bit(blind_data.shift_minus, 1)

        self.shift_reg.write_buffer()

        time.sleep(blind_data.rot_time)

        self.shift_reg.set_buf_bit(blind_data.shift_plus, 0)
        self.shift_reg.set_buf_bit(blind_data.shift_minus, 0)

        self.shift_reg.write_buffer()

        return True

    def turn_light(self, room_name, to_state):
        """
        Включение или выключение света
        :param room_name: имя комнаты, строка
        :param to_state: включить либо выключить свет
        :return: True - успешно, False - неуспешно
        """
        if type(room_name) != str:
            raise ValueError('room_name must be a string')

        elif room_name not in self.room_led_shifts:
            raise ValueError('unable to find the room with such name')

        elif to_state not in self.STATES:
            raise ValueError('wrong action with lights')

        led_data = self.room_led_shifts.get(room_name)

        if to_state == self.ON:
            self.shift_reg.set_buf_bit(led_data, 1)

        elif to_state == self.OFF:
            self.shift_reg.set_buf_bit(led_data, 0)

        else:
            raise ValueError('Unknown action')

        self.shift_reg.write_buffer()

        return True

    def turn_cooler(self, cooler_id, to_state):
        if cooler_id != str:
            raise ValueError('Value must be a string literal')

        if cooler_id not in self.coolers_shifts:
            raise ValueError('Cooler name is not found')

        cooler_data = self.coolers_shifts.get(cooler_id)

        if to_state == self.ON:
            self.shift_reg.set_buf_bit(cooler_data, 1)

        elif to_state == self.OFF:
            self.shift_reg.set_buf_bit(cooler_data, 0)

        else:
            raise ValueError('Unknown action')

        self.shift_reg.write_buffer()
