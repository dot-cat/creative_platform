##############################################################################################
# FIXME List:
# CC1 - Consider Change 1
#   toggle переключает только между стабильными состояниями. Возможно, нужно добавить и
#   переключение между нестабильными состояниями ('открывается' <-> 'закрывается').
#   Но при этом нужно быть внимательным. Нельзя допустить открываение/закрывание слайдера
#   наполовину из-за того, что один из процессов остановит дверь раньше времени.
##############################################################################################

from enum import Enum

from dpl.things.abstract import AbsThing


class AbsSlider(AbsThing):
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
        undefined = None

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    def open(self):
        """
        Открывает слайдер
        :return None
        """
        raise NotImplementedError

    def close(self):
        """
        Закрывает слайдер
        :return None
        """
        raise NotImplementedError

    def toggle(self):
        """
        Переключает состояние слайдера в противоположное:
        открывает закрытый, закрывает открытый
        :return None
        """
        if self.get_state() == self.States.opened:  # Если слайдер открыт...
            self.close()  # закрываем его

        elif self.get_state() == self.States.closed:  # Если слайдер закрыт...
            self.open()  # открываем его

        # Fixme CC1:
        else:  # Если слайдер открывается или закрывается...
            pass  # игнорируем команду
