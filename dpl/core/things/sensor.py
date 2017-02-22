from dpl.core.things import Thing


class Sensor(Thing):
    """
    Базовый абстрактный класс для всех объектов системы ("вещей"),
    которые НЕ могут выполнять операции
    """

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    @property
    def commands(self) -> tuple:
        """
        Список доступных команд. У сенсоров нет доступных команд
        :return: empty tuple
        """
        return ()
