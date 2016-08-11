import RPi.GPIO as GPIO
import time
import logging


class ShiftRegister(object):
    def __init__(self, si, sck, rck, sclr, num_of_slaves=0):  # обьявляем конструктор
        """
        Конструктор объекта
        :param si: номер пина для данных
        :param sck: номер пина для синхросигнала
        :param rck: номер пина для синхросигнала
        :param sclr: номер пина для очистки содержимого регистра
        :param num_of_slaves: количество зависимых сдвиговых регистров
        :return: None
        """
        # проверка на правильность входных значений
        if type(si) != int or type(sck) != int or type(rck) != int or type(sclr) != int:
            raise ValueError('All arguments (port numbers) must be integers')

        logging.debug("{0} init started".format(self))

        self.si = si      # инициализация поля
        self.clk = sck    # инициализация поля
        self.rck = rck    # инициализация поля
        self.sclr = sclr  # инициализация поля
        self.num_of_digits = (num_of_slaves + 1) * 8  # Разрядность сбирки из регистров

        GPIO.setup(self.si, GPIO.OUT)    # Установка пина подачи данных на выход
        GPIO.setup(self.rck, GPIO.OUT)   # Установка пина сдвига на выход
        GPIO.setup(self.clk, GPIO.OUT)   # Установка пина синхросигнала на выход
        GPIO.setup(self.sclr, GPIO.OUT)  # Установка пина очистки на выход

        logging.debug("{0} init finished".format(self))

        return

    def __del__(self):
        """
        Деструктор объекта: освобождение занятых ресурсов
        :return:
        """
        logging.debug("{0} destruction started".format(self))

        self.clear()          # Очищаем содержимое регистра
        self.pulse(self.rck)  # Обновляем содержимое регистров хранения, выставлем все порты регистра в ноль
        self.set_zero()       # подаем на все пины нули
        GPIO.cleanup()        # освобождаем порты

        logging.debug("{0} destruction finished".format(self))
        return

    def set_zero(self):
        """
        Установка всех выводов в ноль
        :return: none
        """
        GPIO.output(self.si,   GPIO.LOW)  # Устанавливаем пин в логический ноль
        GPIO.output(self.rck,  GPIO.LOW)  # Устанавливаем пин в логический ноль
        GPIO.output(self.clk,  GPIO.LOW)  # Устанавливаем пин в логический ноль
        GPIO.output(self.sclr, GPIO.LOW)  # Устанавливаем пин в логический ноль
        return

    def pulse(self, pin):
        """
        Дергаем пин: подаем сначала ноль, потом - единицу, потом опять ноль
        :param pin: пин, который мы дергаем
        :return: none
        """
        GPIO.output(pin, GPIO.LOW)   # подаем на пин логичиеский 0
        time.sleep(0.01)
        GPIO.output(pin, GPIO.HIGH)  # подаем на пин логичискую 1
        time.sleep(0.01)
        GPIO.output(pin, GPIO.LOW)   # подаем на пин логичиеский 0
        return

    def clear(self):
        """
        Очистка содержимого регистра
        :return: none
        """
        GPIO.output(self.sclr, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self.sclr, GPIO.HIGH)
        return

    def write_data(self, data):
        """
        Запись данных во сдвиговый регистр
        :param data: 8 бит данных
            Например:
            0000 0000 0000 0001 - выдать единицу на пин A главного регистра
            0000 0000 0000 1001 - выдать единицу на пины A и D главного регистра
            0000 1001 0000 0000  - выдать единицу на пины A и D первого зависимого регистра
        :return: none
        """
        if data >= (1 << self.num_of_digits):
            raise ValueError(
                'Number of bits in data can\'t exceed {0} bits'.format(self.num_of_digits)
            )

        # Очищаем содержимое регистра
        self.clear()

        # Маска для выборки старшего бита (most significant bit)
        msb_mask = 1 << (self.num_of_digits - 1)

        for i in range(0, self.num_of_digits):  # Обрабатываем 8*N битов
            if data & msb_mask:  # Проверяем старший бит, если он равен единице...
                GPIO.output(self.si, GPIO.HIGH)  # ...то отправляем единицу в регистр
            else:
                GPIO.output(self.si, GPIO.LOW)   # ...иначе отправляем ноль

            self.pulse(self.clk)  # Выполняем сдвиг содержимого регистра

            data <<= 1  # Сдвигаем данные влево на один разряд

        self.pulse(self.rck)  # Фиксируем значения
        return
