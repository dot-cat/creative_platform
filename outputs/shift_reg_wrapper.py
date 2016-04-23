#!/usr/bin/env python
# -*- coding: utf-8 -*-

from shift_reg_lib import ShiftRegister


class ShiftRegWrapper(ShiftRegister):
    """
    ShiftRegWrapper - оболочка для сдвиговорого регистра.
    Содержит дополнительный буфер содержимого и дополнительные методы для работы с ним
    """
    def __init__(self, si, sck, rck, sclr, num_of_slaves=0):
        ShiftRegister.__init__(self, si, sck, rck, sclr, num_of_slaves)
        self.buffer = 0x0
        return

    def get_buf_bit(self, bit_num):
        """
        Считывание значения бита из буфера
        :param bit_num: номер бита, значение которого необхожимо считать
        :return: none
        """
        if bit_num < 0:
            raise ValueError('Bit number must be positive or zero')
        copy_current_state = self.buffer

        if (copy_current_state >> bit_num) & 1:
            return 1
        else:
            return 0

    def set_buf_bit(self, bit_num, value):
        """
        Установка значения бита в буфере.
        Требует выполнения write_current_state для применения изменений
        :param bit_num: номер (позиция) бита
        :param value: значение бита в позиции bit_num
        :return: none
        """
        if bit_num < 0:
            raise ValueError('Bit number must be positive or zero')

        if value != 0 and value != 1:
            raise ValueError('Value must be 1 or zero, True or False')

        if value == 0:
            self.buffer &= ~(1 << bit_num)
        else:
            self.buffer |= (1 << bit_num)
        return

    def write_buffer(self):
        """
        Записать текущее содержимое буфера в регистр
        :return: none
        """
        ShiftRegister.write_data(self, self.buffer)

    def get_buffer(self):
        """
        Получение копии буфера
        :return: целочисленное значение - последовательность нулей и единиц
        """
        return self.buffer

    def write_data(self, data):
        """
        Непосредственная запись в регистр с обновлением буфера
        :param data: записываемые данные
        :return: none
        """
        self.buffer = data
        self.write_buffer()
