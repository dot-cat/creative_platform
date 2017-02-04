#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Started loading libs...")

from dpl.core.controller import Controller

logging.debug("Libs loading finished.")

if __name__ == "__main__":
    controller = Controller()
    controller.run_api()
