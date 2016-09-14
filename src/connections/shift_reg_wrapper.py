import threading
import logging

from connections.shift_reg import ShiftRegister


class ShiftRegWrapper(ShiftRegister):
    """
    ShiftRegWrapper - оболочка для сдвиговорого регистра.
    Содержит дополнительный буфер содержимого и дополнительные методы для работы с ним
    """
    def __init__(self, si, sck, rck, sclr, num_of_slaves=0):
        super().__init__(si, sck, rck, sclr, num_of_slaves)
        self.buffer = 0x0  # Начальное состояние буфера
        self.lock_write = threading.Lock()  # Блокировка для записи из других потоков

    def check_bit_pos(self, bit_pos):
        if not isinstance(bit_pos, int):
            raise ValueError('Bit number must be an integer')

        if bit_pos < 0:
            raise ValueError('Bit number must be positive or zero')

        capacity = self.get_capacity()

        if bit_pos >= capacity:
            raise ValueError('Bit position can\'t be bigger than '
                             'register capacity ({0})'.format(capacity))

    def get_buf_bit(self, bit_pos):
        """
        Считывание значения бита из буфера
        :param bit_pos: номер бита, значение которого необхожимо считать
        :return: none
        """
        self.check_bit_pos(bit_pos)

        return (self.buffer >> bit_pos) & 1

    def set_buf_bit(self, bit_pos, value):
        """
        Установка значения бита в буфере.
        Требует выполнения write_current_state для применения изменений
        :param bit_pos: номер (позиция) бита
        :param value: значение бита в позиции bit_num
        :return: none
        """
        self.check_bit_pos(bit_pos)

        if value == 0:
            self.buffer &= ~(1 << bit_pos)
        elif value == 1:
            self.buffer |= (1 << bit_pos)
        else:
            raise ValueError('Value must be 1 or zero, True or False')
        return

    def write_buffer(self):
        """
        Записать текущее содержимое буфера в регистр
        :return: none
        """
        logging.debug("{0}: write planned. Data: {1}".format(self, bin(self.buffer)))

        with self.lock_write:  # Блокируем запись из других потоков
            ShiftRegister.write_data(self, self.buffer)

        logging.debug("{0}: write finished".format(self))

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
