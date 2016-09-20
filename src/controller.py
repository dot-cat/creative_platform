import RPi.GPIO as GPIO
import logging

import utils.debug_refs as debug_refs

from subsystems.controller_controllables import ControllerControllables
from subsystems.controller_handlers import ControllerHandlers
from subsystems.controller_listeners import ControllerListeners

from model import Model

from events.event_hub import EventHub

##############################################################################################
# FIXME List:
# CC7 - Consider Change 7
#   Метод do_action() ничего не возвращает. Возможно, следует этот факт изменить. Варианты:
#   * выкидывать наружу возращаемое значение вызванного метода;
#   * возвращать 0 при успехе и другие значения при ошибке;
#   * оставить как есть, ничего не возвращать, выбрасывать исключения в случае ошибки.
# CC8 - Consider Change 8
#   Сейчас действия выполняются только над controllable'ами. Может разрешить выполнение
#   действий и над другими объектами? Но тогда нужно реализовать TD2
# TD2 - To Do 2
#   Сделать полноценную реализацию проверки разрешений на выполнение действия.
##############################################################################################


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        logging.debug("{0} init started".format(self))

        self.model = Model("./configs")
        self.model_data = self.model.get_config_data()

        self.controllables = ControllerControllables(self.model_data)
        self.handlers = ControllerHandlers(self.model_data, self.controllables)
        self.__init_event_hub()
        self.listeners = ControllerListeners(self.event_hub)

        logging.debug("{0} init finished".format(self))

    def __del__(self):
        """
        Деструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        logging.debug("{0} destruction started".format(self))

        debug_refs.print_referrers(self.listeners)
        debug_refs.print_referrers(self.event_hub)
        debug_refs.print_referrers(self.handlers)
        debug_refs.print_referrers(self.controllables)

        del self.listeners
        del self.event_hub
        del self.handlers
        del self.controllables

        logging.debug("{0} destruction finished".format(self))

    def __init_event_hub(self):
        self.event_hub = EventHub()

        self.handlers.register_all_handlers(self.event_hub)
