from outputs_dummy.outputs import Outputs
import serial


def input_watcher():
    """
    Метод, ждет события на некотором пине, считывает значения, запускает реакцию
    :return: none
    """
    

class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        self.outputs = Outputs()
        self.serial = serial.Serial('/dev/ttyUSB0')

    def __del__(self):
        """
        Конструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        self.serial.close()
