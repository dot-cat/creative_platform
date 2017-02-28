#!/usr/bin/env python

import logging

from dpl.core.controller import Controller

LOGGER = logging.getLogger("dpl")
LOGGER.setLevel(logging.DEBUG)

if __name__ == "__main__":
    controller = Controller()
    controller.run_api()
    controller.disable_all_things()
