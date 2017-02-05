##############################################################################################
# FIXME List:
#
##############################################################################################

from enum import Enum

from dpl.core.connections import Connection


class Thing(object):
    """
    Базовый абстрактный класс для всех объектов системы ("вещей")

    Гарантии:
    * текущее состояние объекта храниться в буфере
    * текущее состояние обновляется автоматически и всегда актуально
    * состояние объекта не изменяется, если подключение потеряно
    * при обновлении состояния объект оповещает об этом всех подписчиков
    * объект обладает свойствами is_available и last_seen
    * is_available обозначает готовность объекта к приему команд и/или
      считыванию новых значений
    * last_seen - время, когда объект был доступен
    * обладает методами disable и enable
    * disable переводит объект в состояние "недоступен" и
      останавливает автоматическое обновление состояния
    * enable инициирует восстановление соединения и, как следствие,
      переводит объект в состояние "доступен"
    * обладает свойством extended_info, в котором содержится расширенная
      информация о текущем состоянии (например, текущее значение сенсора,
      текущий трек и плейлист плеера и т.д.)
    * extended_info может вернуть None
    """

    class States(Enum):
        """
        Возможные состояния объекта,
        переопределяется в каждом из наследников
        """
        unknown = None

    def __init__(self, con_instance: Connection, con_params: object, metadata: dict=None):
        """
        Конструктор
        :param con_instance: экземпляр соединения
        :param con_params: параметры доступа к соединению
        :param metadata: метаданные объекта (см. свойство metadata)
        """
        self.__con_instance = con_instance
        self.__con_params = con_params
        self.__metadata = metadata
        self.__on_update = None
        self.__on_avail_update = None

    @property
    def metadata(self) -> dict or None:
        """
        Метаданные объекта. Например: ID, название, описание и т.д.
        :return: словарь с метаданными либо None
        """
        return self.__metadata

    @property
    def state(self) -> States:
        """
        Текущее состояние объекта
        :return: объект типа self.States
        """
        raise NotImplementedError

    @property
    def is_available(self) -> bool:
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        raise NotImplementedError

    @property
    def last_seen(self) -> float:
        """
        Возвращает время, когда объект был доступен в последний раз
        :return: float, UNIX time
        """
        raise NotImplementedError

    @property
    def extended_info(self) -> dict or None:
        """
        Возвращает расширенную информацию о состоянии объекта
        :return: словарь с информацией либо None
        """
        raise NotImplementedError

    @staticmethod
    def __is_good_callback(func) -> bool:
        return isinstance(func, callable) or func is None

    @property
    def on_update(self) -> callable:
        return self.__on_update

    @on_update.setter
    def on_update(self, func):
        if self.__is_good_callback(func):
            self.__on_update = func

    @property
    def on_avail_update(self) -> callable:
        return self.__on_avail_update

    @on_avail_update.setter
    def on_avail_update(self, func):
        if self.__is_good_callback(func):
            self.__on_avail_update = func

    def disable(self) -> None:
        """
        Отключает объект, останавливает обновление состояния и
        делает его неактивным
        :return: None
        """
        raise NotImplementedError

    def enable(self) -> None:
        """
        Включает объект, запускает обновление состояние и делает
        его активным
        :return: None
        """
        raise NotImplementedError


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
