"""
Модуль с базовой реализацией соединения.

Каждое соединение должно:
* наследоваться от типа Connection
* иметь соответсвующую фабрику, которая наследуется от
  ConnectionFactory
* добавлять экземпляр фабрики в реестр ConnectionRegistry

Пример:
# Подключение реестра
from dpl.connections.connection_registry import ConnectionRegistry

# Объявление наследника Connection
# Объявление наследника ConnectionFactory

# Регистрация фабрики в реестре
ConnectionRegistry.register_factory(
    "abs_connection",
    ConnectionFactory()
)

См. также: класс MPDClientConnection
"""

from enum import IntEnum


class Connection(object):
    """
    Connection (соединение)

    Абстракция всех соединений между устройствами в программе

    Свойства:
    * имеет индикацию состояния соединения:
      CONNECTED, CONNECTING, DISABLED

    Гарантии:
    * после создания находится в состоянии DISABLED
    * при неожиданном разрыве - переходит в состояние CONNECTING
      и пытается восстановить соединение
    * если данные по соединению не могут быть переданы -
      возвращается код ошибки
    * вызов метода connect игнориуется, если соединение уже активно
      (CONNECTED или CONNECTING)
    * вызов метода disconnect игнорируется, если соединение уже выключено
      (DISABLED)
    """
    class States(IntEnum):
        DISABLED = -1  # Соединение выключено, восстановление не происходит
        CONNECTING = 0  # Соединение активно, идет установка соединения
        CONNECTED = 1  # Соединение активно, восстановлено и готово к работе

    def set_connect_params(self, *args, **kwargs):
        """
        Устанавливает параметры запуска соединения
        :param args, kwargs: параметры, которые нужны для запуска соединения
        :return: None
        """
        raise NotImplementedError

    def connect(self, *args, **kwargs) -> None:
        """
        Переводит соединение из пассивного в активное состояние
        :return: None
        """
        raise NotImplementedError

    def reconnect(self) -> None:
        """
        Переводит соединение из пассивного в активное состояние
        с восстановлением настроек
        :return: None
        """
        raise NotImplementedError

    def disconnect(self) -> None:
        """
        Переводит соединение в пассивное состояние
        :return: None
        """
        raise NotImplementedError

    @property
    def state(self) -> States:
        """
        Текущее состояние соединения
        :return: Connection.States
        """
        raise NotImplementedError


class ConnectionFactory(object):
    """
    Фабрика соединений. Абстрактный класс, который содержит
    единственный метод build
    """
    @staticmethod
    def build(config: dict) -> Connection:
        """
        Метод, который возвращает готовый объект типа Connection,
        построенный на основе заданной конфигурации
        :param config: словарь, конфигурация
        :return: экземпляр типа Connection
        """
        raise NotImplementedError

