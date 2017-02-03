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


class Connection(object):
    """
    Соединение. Абстрактный класс соединений (подключений) в программе.
    Соединения являются средой, через которую идет передача данных
    между контроллером (устройством с DPL) и объектами (things)
    """
    pass


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


"""

"""
