from dpl.connections.abs_connection import ConnectionFactory


class ConnectionRegistry(object):
    """
    Класс (Singleton по задумке), который хранит список фабрик
    для всех импортированных соединений
    """
    __reg = dict()

    @classmethod
    def register_factory(cls, alias: str, factory: ConnectionFactory) -> None:
        """
        Реестрация фабрики подключений
        :param alias: псевдоним типа подключения, который используется в конфиг-файлах
        :param factory: экземпляр фабрики
        :return: None
        """
        cls.__reg[alias] = factory

    @classmethod
    def resolve_factory(cls, alias: str, default=None) -> ConnectionFactory:
        """
        Получение объекта-фабрики по псевдониму
        :param alias: псевдоним типа подключения, который используется в конфиг-файлах
        :param default: возвращаемое значение по умолчанию
        :return: объект типа ConnectionFactory
        """
        return cls.__reg.get(alias, default)

    @classmethod
    def remove_factory(cls, alias: str, default=None) -> ConnectionFactory:
        """
        Удаление объекта-фабрики по псевдониму
        :param alias: псевдоним типа подключения, который используется в конфиг-файлах
        :param default: возвращаемое значение по умолчанию
        :return: объект типа ConnectionFactory, удаленная фабрика
        """
        return cls.__reg.pop(alias, default)

