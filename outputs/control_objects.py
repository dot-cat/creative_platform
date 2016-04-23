#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shift_reg_wrapper import ShiftRegWrapper
from enum import Enum
import time


def check_shift_reg_type(shift_reg):
    if type(shift_reg) != ShiftRegWrapper:
        raise ValueError('type of shift_reg value must be a ShiftRegWrapper')


class Trigger(object):
    """
    Объект с двумя состояниями: включено и выключено.
    Во включенном состоянии записывает 1-цу в регистр,
    в выключенном - ноль
    """

    class States(Enum):
        """
        Возможные состояния переключателя
        """
        on = True
        off = False

    def __init__(self, shift_reg, bit_pos):
        """
        Конструктор
        :param shift_reg: сдвиговый регистр, в котором хранится текущее состояние
        :param bit_pos: позиция бита, который контролирует объект
        :return: None
        """
        check_shift_reg_type(shift_reg)

        self.shift_reg = shift_reg
        self.bit_pos = bit_pos

    def get_state(self):
        """
        Получение текущего состояния переключателя
        :return: значение типа Trigger.States
        """
        return self.States(self.shift_reg.get_buf_bit(self.bit_pos))

    def __set_state(self, state):
        """
        Установка состояния объекта и запись состояния в буфер
        :param state: желаемое состояние
        :return: None
        """
        assert self.States.on == True and self.States.off == False,\
            'state code changed, update this function before usage'

        if type(state) != self.States:
            raise ValueError('Type of state argument must be a Trigger.State')

        self.shift_reg.set_buf_bit(self.bit_pos, state)
        return

    def set_on(self):
        """
        Включение объекта
        :return: none
        """
        self.__set_state(self.States.on)
        return

    def set_off(self):
        """
        Выключение объекта
        :return: none
        """
        self.__set_state(self.States.off)
        return

    def apply_state(self):
        """
        Принудительная запись содержимого буфера в регистр
        :return: None
        """
        self.shift_reg.write_buffer()


class Slider(object):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается
    """
    class States(Enum):
        """
        Возможные состояния выдвигающегося элемента
        """
        closed  = [0, 0]
        closing = [0, 1]
        opening = [1, 0]
        opened  = [1, 1]

    def __init__(self, shift_reg, bit_plus, bit_minus, switch_time=1):
        """
        Конструктор
        :param shift_reg: регистр, в котором хранится текущее состояние
        :param bit_plus: позиция бита, который отвечает за положительный вывод мотора
        :param bit_minus: позиция бита, который отвечает за отрицательный вывод мотора
        :param switch_time: время переключения между двумя состояниями в секундах
        :return: None
        """
        check_shift_reg_type(shift_reg)

        if switch_time <= 0:
            raise ValueError('switch_time must be bigger than zero')

        self.shift_reg = shift_reg
        self.bit_plus = bit_plus
        self.bit_minus = bit_minus
        self.switch_time = switch_time

    def get_state(self):
        return self.States(
            [
                self.shift_reg.get_buf_bit(self.bit_plus),
                self.shift_reg.get_buf_bit(self.bit_minus)
            ]
        )

    def __set_state(self, state):
        if type(state) != self.States:
            raise ValueError('Type of state argument must be a Slider.State')

        self.shift_reg.set_buf_bit(self.bit_plus, state[0])
        self.shift_reg.set_buf_bit(self.bit_minus, state[1])

    def __apply_state(self):
        self.shift_reg.write_buffer()
        return

    def open(self):
        if self.shift_reg.get_buf_bit(self.bit_plus) == 1:
            pass

        else:
            self.__set_state(self.States.opening)
            self.__apply_state()

            time.sleep(self.switch_time)

        self.__set_state(self.States.opened)

        self.__apply_state()

    def close(self):
        if self.shift_reg.get_buf_bit(self.bit_plus) == 0:
            pass

        else:
            self.__set_state(self.States.closing)
            self.__apply_state()

            time.sleep(self.switch_time)

        self.__set_state(self.States.closed)

        self.__apply_state()


class Door(Slider):
    pass


class Blinds(Slider):
    pass


class Light(Trigger):
    pass


class Cooler(Trigger):
    pass