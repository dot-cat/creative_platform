from dpl.core.things import Thing, ThingFactory


class ThingRegistry(object):
    """
    Класс (Singleton по задумке), который хранит список фабрик
    для всех импортированных соединений
    """
    __reg = dict()  # type: dict[str, dict[type, ThingFactory]]

    @classmethod
    def register_factory(cls, type_alias: str, con_type: type, factory: ThingFactory) -> None:
        """
        Регистрация фабрики подключений
        :param type_alias: псевдоним типа объекта, который используется в конфиг-файлах
        :param con_type: тип используемого подключения
        :param factory: экземпляр фабрики
        :return: None
        """
        type_reg = cls.__reg.setdefault(type_alias, dict())  # type: dict[type, ThingFactory]
        type_reg[con_type] = factory

    @classmethod
    def resolve_factory(cls, type_alias: str, con_type: type, default=None) -> ThingFactory:
        """
        Получение объекта-фабрики по псевдониму типа вещи и типу соединения
        :param type_alias: псевдоним типа объекта, который используется в конфиг-файлах
        :param con_type: тип используемого подключения
        :param default: возвращаемое значение по умолчанию
        :return: объект типа ThingFactory
        """
        type_reg = cls.__reg.get(type_alias)

        if type_reg is None:
            return default

        return type_reg.get(con_type, default)

    @classmethod
    def has_type(cls, type_alias: str) -> bool:
        """
        Проверка на наличие зарегистрированного типа
        :param type_alias: псевдоним типа объекта
        :return: bool, наличие типа в реестре
        """
        return type_alias in cls.__reg

    @classmethod
    def remove_factory(cls, type_alias: str, con_type: type, default=None) -> ThingFactory:
        """
        Удаление объекта-фабрики по псевдониму
        :param type_alias: псевдоним типа объекта, который используется в конфиг-файлах
        :param con_type: тип используемого подключения
        :param default: возвращаемое значение по умолчанию
        :return: объект типа ThingFactory, удаленная фабрика
        """
        type_reg = cls.__reg.get(type_alias)

        if type_reg is None:
            return default

        return type_reg.pop(con_type, default)
