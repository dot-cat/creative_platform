import RPi.GPIO as GPIO
import time

from shift_reg_lib import ShiftRegister


# устанавливаем пины
si = 37  # пин для входных данных
rck = 33  # пин для сдвига регистров хранения
sck = 35  # пин для синхросигнала и сдвига
sclr = 40  # пин для очистки

WorkRegistr = ShiftRegister(si, sck, rck, sclr)


class PolarElement(object):
    def __init__(self, shift_plus, shift_minus):
        self.shift_plus = shift_plus
        self.shift_minus = shift_minus
        return


class Outputs(object):
    # Константы:
    ON  = True
    OFF = False
    STATES = [ON, OFF]

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, нееобходимых для вывода
        :return: none
        """

        self.door_1_plus  = 16 #0
        self.door_1_minus = 17 #1
        self.door_2_plus  = 18 #2
        self.door_2_minus = 19 #3
        self.diode_1 = 20 #4
        self.diode_2 = 21 #5
        self.door_3_plus  = 22 #6
        self.door_3_minus = 23 #7
        self.door_4_plus  = 8 #8
        self.door_4_minus = 9 #9
        self.diode_3 = 10 #10
        self.diode_4 = 11 #11
        self.blind_1_plus  = 12 #12
        self.blind_1_minus = 13 #13
        self.blind_2_plus  = 14 #14
        self.blind_2_minus = 15 #15
        self.blind_3_plus  = 0 #16
        self.blind_3_minus = 1 #17
        self.diode_5 = 2 #18
        self.diode_6 = 3 #19
        self.cooler  = 4 #20

        self.current_state = 0x0

        self.door_shifts = {
                              'First door':   PolarElement(self.door_1_plus, self.door_1_minus),
                              'Second door':  PolarElement(self.door_2_plus, self.door_2_minus),
                              'Third door':   PolarElement(self.door_3_plus, self.door_3_minus),
                              'Fourth door':  PolarElement(self.door_4_plus, self.door_4_minus)
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
                               'First blind':  PolarElement(self.blind_1_plus, self.blind_1_minus),
                               'Second blind': PolarElement(self.blind_2_plus, self.blind_2_minus),
                               'Third blind':  PolarElement(self.blind_3_plus, self.blind_3_minus)
                            }


        return

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

        if self.check_bit(door_data.shift_plus) == 1:
            self.set_bit(door_data.shift_plus,  1)
            self.set_bit(door_data.shift_minus, 1)

        else:
            self.set_bit(door_data.shift_plus,  1)
            self.set_bit(door_data.shift_minus, 0)

        WorkRegistr.write_data(self.current_state)

        time.sleep(10)

        self.set_bit(door_data.shift_plus,  1)
        self.set_bit(door_data.shift_minus, 1)

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

        if self.check_bit(door_data.shift_plus) == 0:
            self.set_bit(door_data.shift_plus,  0)
            self.set_bit(door_data.shift_minus, 0)

        else:
            self.set_bit(door_data.shift_plus,  0)
            self.set_bit(door_data.shift_minus, 1)

        WorkRegistr.write_data(self.current_state)

        time.sleep(10)

        self.set_bit(door_data.shift_plus,  0)
        self.set_bit(door_data.shift_minus, 0)

        WorkRegistr.write_data(self.current_state)

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

        if self.check_bit(blind_data.shift_plus) == 1:
            self.set_bit(blind_data.shift_plus,  1)
            self.set_bit(blind_data.shift_minus, 1)

        else:
            self.set_bit(blind_data.shift_plus,  1)
            self.set_bit(blind_data.shift_minus, 0)

        WorkRegistr.write_data(self.current_state)

        time.sleep(10)

        self.set_bit(blind_data.shift_plus,  1)
        self.set_bit(blind_data.shift_minus, 1)

        WorkRegistr.write_data(self.current_state)

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

        if self.check_bit(blind_data.shift_plus) == 0:
            self.set_bit(blind_data.shift_plus,  0)
            self.set_bit(blind_data.shift_minus, 0)

        else:
            self.set_bit(blind_data.shift_plus,  0)
            self.set_bit(blind_data.shift_minus, 1)

        WorkRegistr.write_data(self.current_state)

        time.sleep(10)

        self.set_bit(blind_data.shift_plus,  0)
        self.set_bit(blind_data.shift_minus, 0)

        WorkRegistr.write_data(self.current_state)

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
            self.set_bit(led_data, 1)

        elif to_state == self.OFF:
            self.set_bit(led_data, 0)

        else:
            raise ValueError('Unknown action')

        WorkRegistr.write_data(self.current_state)

        return True

    def turn_cooler(self, cooler_id, to_state):
        if cooler_id != str:
            raise ValueError('Value must be a string literal')

        if cooler_id not in self.coolers_shifts:
            raise ValueError('Cooler name is not found')

        cooler_data = self.coolers_shifts.get(cooler_id)

        if to_state == self.ON:
            self.set_bit(cooler_data, 1)

        elif to_state == self.OFF:
            self.set_bit(cooler_data, 0)

        else:
            raise ValueError('Unknown action')

        WorkRegistr.write_data(self.current_state)

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

        if (copy_current_state >> bit_num) & 1:
            return 1
        else:
            return 0

