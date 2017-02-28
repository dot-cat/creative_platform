#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################################
# FIXME List:
# CC8 - Consider Change 8
#   Сейчас действия выполняются только над Thing'ами. Может разрешить выполнение
#   действий и над другими объектами? Но тогда нужно реализовать TD2
# CC19 - Consider Change 19
#   Сделать функцию более опрятной
# TD2 - To Do 2
#   Сделать полноценную реализацию проверки разрешений на выполнение действия.
# TD4 - To Do 4
#   Сделать путь к конфиг-файлах изменяемым
# DH3 - Dirty Hack 4
#   Вынести обработку core-параметров в отдельный блок, убрать полный перебор или сделать
#   его резонным
##############################################################################################

import logging

import dpl.utils.debug_refs as debug_refs
from dpl.core.config import Config
from dpl.core.message_hub import MessageHub
from dpl.libs.gpio_chooser import GPIO
from dpl.subsystems.controller_handlers import ControllerHandlers
from dpl.subsystems.controller_listeners import ControllerListeners
from dpl.subsystems.controller_things import ControllerThings

LOGGER = logging.getLogger(__name__)


class Controller(object):
    def __init__(self):
        """
        Конструктор, выполняет инициализацию и запуск всего и вся
        :return: none
        """
        GPIO.setmode(GPIO.BOARD)

        LOGGER.debug("%s init started", self)

        self.model = Config("../configs")  # FIXME: TD4

        self.things = ControllerThings(self.model)
        self.handlers = ControllerHandlers(self.model, self.things)
        self.__init_msg_hub()
        self.listeners = ControllerListeners(self.msg_hub)

        LOGGER.debug("%s init finished", self)

    def disable_all_things(self):
        self.things.disable_all()

    def __del__(self):
        """
        Деструктор, выполняет освобождение и остановку всего и вся
        :return: none
        """
        LOGGER.debug("%s destruction started", self)

        debug_refs.print_referrers(self.listeners)
        debug_refs.print_referrers(self.msg_hub)
        debug_refs.print_referrers(self.handlers)
        debug_refs.print_referrers(self.things)

        del self.listeners
        del self.msg_hub
        del self.handlers
        del self.things

        LOGGER.debug("%s destruction finished", self)

    def __init_msg_hub(self):
        self.msg_hub = MessageHub()

        self.handlers.register_all_handlers(self.msg_hub)

    # FIXME: DH4
    def __get_api_params(self) -> dict:
        core_params = self.model.get_category_config("core")

        for item in core_params:
            if item["module"] == "rest_api":
                return item

        return None

    # FIXME: CC19
    def run_api(self):
        LOGGER.debug("Loading API libs...")
        import dpl.core.api as api

        LOGGER.debug("API init...")
        api.init(self.model, self.things, self.msg_hub)

        LOGGER.debug("API is ready to run")

        api_params = self.__get_api_params()

        if api_params is None:
            LOGGER.warning("REST API settings not found, "
                           "falling back to default API settings")
            api.run(debug=True, use_reloader=False)
        else:
            api.run(
                host=api_params.get("host"),
                debug=True,
                port=api_params.get("port"),
                use_reloader=False
            )
