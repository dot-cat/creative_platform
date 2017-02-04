##############################################################################################
# FIXME List:
# CC2 - Consider Change 2
#   Методы не возвращают результат совего выполнения (успешно/неуспешно). Возможно, нужно 
#   добавить индикацию статуса выполнения
# CC12 - Consider Change 12
#   Плохо переносится на код на С++
##############################################################################################

from enum import Enum
from dpl.core.connections import Connection


class Thing(object):
    """
    Базовый абстрактный класс для всех контролируемых объектов
    """

    class States(Enum):
        """
        Возможные состояния объекта
        """
        on = True
        off = False
        undefined = None

    def __init__(self, con_instance: Connection, con_params, metadata=None):
        """
        Инициализация контроллируемого объекта
        :param con_instance: экземпляр connection'а
        :param con_params: параметры доступа к connection'у
        :param metadata: метеданные (имя, описание, тип объекта)
        """
        self.con_instance = con_instance
        self.con_params = con_params
        self.metadata = metadata

        # Строку ниже добавляйте сами, если connections не обеспечивает буффер
        # self.curr_state = self.States.undefined

    def set_state(self, target_state):
        """
        Немедленно установить конкретное состояние
        :param target_state: значение из self.States, желаемое состояние
        """
        raise NotImplementedError

    def get_state(self) -> States:
        """
        Вернуть свое состояние внешнему миру из буфера
        :return: значение типа self.States
        """
        raise NotImplementedError

    def get_state_string(self) -> str:
        """
        Вернуть свое состояние внешнему миру из буфера. Состояние возращается в виде строки
        :return: str, текущее состояние
        """
        return str(self.get_state().name)  # Fixme: CC12

    def toggle(self):
        """
        Переключить из текущего состояния в противоположное
        """
        raise NotImplementedError

    def get_metadata(self):
        return self.metadata


class ThingFactory(object):
    """
    Фабрика вещей. Абстрактный класс, который содержит
    единственный метод build
    """
    @staticmethod
    def build(con_instance, con_params: dict, metadata: dict=None) -> Thing:
        """
        Метод, который возвращает готовый объект типа Thing,
        построенный на основе заданной конфигурации
        :param con_instance: экземпляр connection'а
        :param con_params: параметры доступа к connection'у
        :param metadata: метеданные (имя, описание, тип объекта)
        """
        raise NotImplementedError
