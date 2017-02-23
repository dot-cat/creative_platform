##############################################################################################
# FIXME List:
# CC24 - Consider Change 24
#   Переименовать cmd в action
# TD5 - To Do 5
#   Переименовать все вхождения command в action
##############################################################################################

from enum import IntEnum

from dpl.core.things import Thing


class Actuator(Thing):
    """
    Базовый абстрактный класс для всех объектов системы ("вещей"),
    которые могут выполнять некоторый набор операций

    Гарантии:
    * выполняемые команды возвращают код ошибки при обрыве соединения
    * позволяет получить список всех доступных команд
    * обладает методом execute, который выполняет одну из доступных команд
    """

    class ExecutionResult(IntEnum):
        """
        Результат выполнения операции
        """
        OK = 0
        IGNORED_BAD_STATE = 1
        IGNORED_UNAVAILABLE = 2

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def actions(self) -> list or tuple:
        """
        Возвращает список всех доступных команд/действий над объектом
        :return: list или tuple
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        """
        Метод, возвращающий копию объекта в виде словаря
        :return: словарь-копия значений из свойств
        """
        result = super().to_dict()  # Свойства базового класса
        result["actions"] = self.actions  # Специфичное поле: доступные действия

        return result

    def execute(self, cmd: str, *args, **kwargs) -> ExecutionResult:  # Fixme: CC24
        """
        Запускает выполнение команды/действия, указанной в cmd
        :param cmd: строка, команда на выполнение
        :param args, kwargs: параметры команды
        :return: возвращаемое значение
        """
        invalid_cmd_error = ValueError("Invalid command: {0}".format(cmd))

        if cmd not in self.actions:
            raise invalid_cmd_error

        cmd_func = self.__getattribute__(cmd)

        if cmd_func is not callable:
            raise invalid_cmd_error

        return cmd_func(*args, **kwargs)

    def toggle(self) -> ExecutionResult:
        """
        Переключает объект между двумя крайними состояниями
        :return: результат выполнения
        """
        raise NotImplementedError
