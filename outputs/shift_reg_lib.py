import RPi.GPIO as GPIO
import time


class ShiftRegister(object):
    def __init__(self, si, sck, rck, sclr):  # обьявляем конструктор
        """
        Конструктор объекта
        :param si: номер пина для данных
        :param sck: номер пина для синхросигнала
        :param rck: номер пина для синхросигнала
        :param sclr: номер пина для очистки содержимого регистра
        :return:
        """
        # проверка на правильность входных значений
        if type(si) != int or type(sck) != int or type(rck) != int or type(sclr) != int:
            raise ValueError('All arguments (port numbers) must be integers')

        self.si = si      # инициализация поля
        self.clk = sck    # инициализация поля
        self.rck = rck    # инициализация поля
        self.sclr = sclr  # инициализация поля

        GPIO.setup(self.si, GPIO.OUT)    # Установка пина подачи данных на выход
        GPIO.setup(self.rck, GPIO.OUT)   # Установка пина сдвига на выход
        GPIO.setup(self.clk, GPIO.OUT)   # Установка пина синхросигнала на выход
        GPIO.setup(self.sclr, GPIO.OUT)  # Установка пина очистки на выход
        return

    def __del__(self):
        """
        Деструктор объекта: освобождение занятых ресурсов
        :return:
        """
        self.clear()          # Очищаем содержимое регистра
        self.pulse(self.rck)  # Обновляем содержимое регистров хранения, выставлем все порты регистра в ноль
        self.set_zero()       # подаем на все пины нули
        GPIO.cleanup()        # освобождаем порты
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
        :return: none
        """
        #if data > 0xFF:
        #    raise ValueError('Number of bits in data can\'t exceed 8 bits')

        # Очищаем содержимое регистра
        self.clear()

        for i in range(0, 24):   # Обрабатываем восемь бит
            if data & 0x800000:  # Проверяем старший бит, если он равен единице...
                GPIO.output(self.si, GPIO.HIGH)  # ...то отправляем единицу в регистр
            else:
                GPIO.output(self.si, GPIO.LOW)   # ...иначе отправляем ноль

            self.pulse(self.clk)  # Выполняем сдвиг содержимого регистра

            data <<= 1  # Сдвигаем переменную с данными на один бит влево

        self.pulse(self.rck)  # Фиксируем значения
        return
