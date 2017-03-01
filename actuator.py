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
    * позволяет получить список всех доступных команд (действий над объектом)
    * обладает свойством is_active, которое обозначает нахождение объекта в одном из
      активных состояний (например: включен, идет проигрывание, идет обнаружение движения и т.д.).
    * свойство is_active зависит только от state и не зависит от is_available
    * обладает методом execute, который выполняет одну из доступных команд
    * обладает методом toggle, который переключает между двумя крайними состояниями
    * обладает методом activate, который переводит объект в одно из активных состояний
    * обладает методом deactivate, который переводит объект в одно из неактивных состояний
    * при выполнении команд/действий возвращается результат выполнения операции
    * при обрыве соединения выполнение команд игнорируется, возвращается соответствующий
      код результата выполнения
    """

    class ExecutionResult(IntEnum):
        """
        Результат выполнения операции
        """
        OK = 0  # OK, команда выполнена успешно
        IGNORED_BAD_STATE = 1  # невозможно применить в текущем состоянии
        IGNORED_UNAVAILABLE = 2  # объект недоступен, соединение потеряно

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param con_instance: экземпляр соединения
        :param con_params: параметры доступа к соединению
        :param metadata: метаданные объекта (см. свойство metadata)
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
        result["is_active"] = self.is_active  # Специфичное поле: является ли текущее состояние активным

        return result

    @property
    def is_active(self) -> bool:
        """
        Находится ли объект в одном из активных состояний
        :return: bool, True or False
        """
        raise NotImplementedError

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
        if self.is_active:
            return self.deactivate()
        else:
            return self.activate()

    def activate(self) -> ExecutionResult:
        """
        Переключает объект в одно из активных состояний
        :return: результат выполнения
        """
        raise NotImplementedError

    def deactivate(self) -> ExecutionResult:
        """
        Переключает объект в одно из НЕактивных состояний
        :return: результат выполнения
        """
        raise NotImplementedError
