import logging
import weakref  # FIXME: DH1
from threading import Thread, Event


##############################################################################################
# FIXME List:
# DH1 - Dirty Hack 1
#   Внутри потока `__waiter_loop` выполняется вечный цикл, который ожидает новые данные.
#   Как результат - поток никогда не завершается, он вечно держит ссылку на `self`, деструктор
#   слушателя никогда не выполняется. И при этом слушатель удерживает `feedback` от удаления.
#
#   Грязный хак состоит в использовании `weakref` на `feedback`. Таким образом `feedback`
#   может быть корректно удален вне зависимости от выполнения деструктора слушателя.
#
#   Возможное решение: переход на процессы и принудительный останов `__waiter_loop`.
##############################################################################################


class Listener(object):
    """
    Слушатель. Базовый класс для всех объектов, которые ожидают некоторые данные,
    считывают и обрабатывают их, а затем выполняют некоторые действия.
    """

    def __init__(self, feedback):
        """
        Инициализация слушателя
        :param feedback: Объект для обратной связи
        """
        logging.debug("%s init started", self)

        self.feedback = weakref.proxy(feedback)  # FIXME: DH1
        self.stop_event = Event()
        self.listener_thread = Thread(target=self.__waiter_loop, daemon=True)

        logging.debug("%s init finished", self)

    def start(self):
        """
        Запуск слушателя
        :return: None
        """
        self.listener_thread.start()

    def __del__(self):
        """
        Деструктор слушателя. Останавливает процессы, освобождает ресурсы
        :return: None
        """
        # FIXME: DH1: Он даже не выполняется в текущем виде

        logging.debug("%s destruction started", self)

        self.stop_event.set()

        logging.debug("%s destruction finished", self)

    def get_data(self):
        """
        Получить очередную порцию данных. Блокирующая функция -
        выполняется до тех пор, пока не получит новую порцию данных.
        :return: полученные "сырые" данные
        """
        raise NotImplementedError

    def process_data(self, raw_data):
        """
        Обработка "сырых" данных
        :param raw_data: считанные данные
        :return: None
        """
        raise NotImplementedError

    def __waiter_loop(self):
        """
        Цикл-слушатель. Считывает данные с помощью get_data и запускает их обработку.
        :return: None
        """
        while not self.stop_event.is_set():
            # Будет ждать, пока пользователь что-то не введет.
            # Даже если self.stop_event.is_set() == True
            data = self.get_data()

            thread = Thread(target=self.process_data, args=(data,), daemon=True)
            thread.start()  # запускаем дочерний поток
