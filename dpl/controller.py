#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import dpl.api as api
import dpl.utils.debug_refs as debug_refs
from dpl.connections.gpio_chooser import GPIO
from dpl.messages.message_hub import MessageHub
from dpl.model import Model
from dpl.subsystems.controller_controllables import ControllerControllables
from dpl.subsystems.controller_handlers import ControllerHandlers
from dpl.subsystems.controller_listeners import ControllerListeners


##############################################################################################
# FIXME List:
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

        logging.debug("%s init started", self)

        self.model = Model("../configs")
        self.model_data = self.model.get_config_data()

        self.controllables = ControllerControllables(self.model)
        self.handlers = ControllerHandlers(self.model, self.controllables)
        self.__init_msg_hub()
        self.listeners = ControllerListeners(self.msg_hub)
        api.init(self.model, self.controllables, self.msg_hub)

        logging.debug("%s init finished", self)

    def __del__(self):
        """
        Деструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        logging.debug("%s destruction started", self)

        debug_refs.print_referrers(self.listeners)
        debug_refs.print_referrers(self.msg_hub)
        debug_refs.print_referrers(self.handlers)
        debug_refs.print_referrers(self.controllables)

        del self.listeners
        del self.msg_hub
        del self.handlers
        del self.controllables

        logging.debug("%s destruction finished", self)

    def __init_msg_hub(self):
        self.msg_hub = MessageHub()

        self.handlers.register_all_handlers(self.msg_hub)

    def start_api(self):
        api.run(host="vostro.lan", debug=True, port=10800, use_reloader=False)
