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

import enum


class ConnectionStatus(enum):
    """
    Возможные состояния соединения
    """
    Connected = 0  # соединение успешно восстановлено
    Connecting = 1  # выполняется восстановление соединения
    Disconnected = 2  # соединение разорвано


class Connection(object):
    """
    Соединение. Абстрактный класс соединений (подключений) в программе.
    Соединения являются средой, через которую идет передача данных
    между контроллером (устройством с DPL) и объектами (things)
    """

    @property
    def status(self) -> ConnectionStatus:
        """
        Получение текущего статуса соединения
        :return: объект типа Connection.Status
        """
        raise NotImplementedError

    @property
    def is_connected(self) -> bool:
        """
        Проверка на то, установлено ли соединение
        :return: true - установлено, false - нет
        """
        return self.status == ConnectionStatus.Connected

    def connect(self) -> None:
        """
        Запуск установки соединения, переход в состояние Connecting
        :return: None
        """
        raise NotImplementedError

    def disconnect(self) -> None:
        """
        Разрыв соединения, переход в состояние Disconnected
        :return: None
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

