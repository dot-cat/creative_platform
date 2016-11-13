##############################################################################################
# FIXME List:
# CCXX19 - Consider Change 19
#   Enum для значений цифровых выходов
# CCXX20 - Consider Change 20
#   Добавить чтение значений с портов GPIO подключенного устройства
##############################################################################################

import serial


class SerialGPIO(object):
    # Fixme: CCXX19
    HIGH = 1
    LOW = 0

    def __init__(self, *args, **kwargs):
        """
        Инициализация последовательного соединения
        """
        self.serial_con = serial.Serial(*args, **kwargs)

    def digital_write(self, pin, value):
        """
        Подача сигнала на выход
        :param pin: id (номер/имя) пина, на который подается сигнал
        :param value: значение, которое необходимо выставить
        :return: None
        """
        if value != SerialGPIO.HIGH and value != SerialGPIO.LOW:
            raise ValueError('Tried to set an invalid value on pin {0}'.format(pin))

        data = "{0} {1}\n".format(pin, value)

        self.serial_con.write(data.encode())
