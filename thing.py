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
    * объект обладает свойствами is_available и last_updated
    * is_available обозначает готовность объекта к приему команд и/или
      считыванию новых значений
    * last_updated - время, когда объект был обновлен
    * обладает методами disable и enable
    * disable переводит объект в состояние "недоступен" и
      останавливает автоматическое обновление состояния
    * enable инициирует восстановление соединения и, как следствие,
      переводит объект в состояние "доступен"
    * наследники могут обладать дополнительными полями, в которых
      содержится расширенная информация о текущем состоянии (например,
      текущее значение сенсора, текущий трек и плейлист плеера и т.д.)

    Классы-наследники могут расширять реализацию и добавлять как новые
    методы, так и новые свойства.
    """

    class States(Enum):
        """
        Возможные состояния объекта,
        переопределяется в каждом из наследников
        """
        unknown = None

    def __init__(self, con_instance: Connection, con_params, metadata: dict=None):
        """
        Конструктор
        :param con_instance: экземпляр соединения
        :param con_params: параметры доступа к соединению
        :param metadata: метаданные объекта (см. свойство metadata)
        """
        self._con_instance = con_instance
        self._con_params = con_params
        self._metadata = metadata
        self._on_update = None
        self._on_avail_update = None

    @property
    def metadata(self) -> dict or None:
        """
        Метаданные объекта. Например: ID, название, описание и т.д.
        :return: словарь с метаданными либо None
        """
        return self._metadata

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
    def last_updated(self) -> float:
        """
        Возвращает время, когда объект был обновлен в последний раз
        :return: float, UNIX time
        """
        raise NotImplementedError

    def to_dict(self) -> dict:
        """
        Метод, возвращающий копию объекта в виде словаря
        :return: словарь-копия значений из свойств
        """
        result = {
            "state": self.state.name,
            "is_available": self.is_available,
            "last_updated": self.last_updated
        }

        result.update(self.metadata)

        return result

    @staticmethod
    def __is_good_callback(func) -> bool:
        return isinstance(func, callable) or func is None

    @property
    def on_update(self) -> callable or None:
        """
        Функтор, который запускается при обновлении свойств объекта
        :return: текущий зарегистрированный функтор
        """
        return self._on_update

    @on_update.setter
    def on_update(self, func: callable or None):
        """
        Устанавливает функтор, который будет вызван при обновлении свойств объекта
        :param func: функтор, принимающий два аргумента:
                     * ссылку на изменившийся объект
                     * информацию об изменении
        :return: None
        """
        if self.__is_good_callback(func):
            self._on_update = func

    @property
    def on_avail_update(self) -> callable:
        """
        Функтор, который запускается при изменении доступности объекта
        :return: текущий зарегистрированный функтор
        """
        return self._on_avail_update

    @on_avail_update.setter
    def on_avail_update(self, func):
        """
        Устанавливает функтор, который будет вызван при изменении доступности объекта
        :param func: функтор, принимающий два аргумента:
                     * ссылку на изменившийся объект
                     * информацию об изменении
        :return: None
        """
        if self.__is_good_callback(func):
            self._on_avail_update = func

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
