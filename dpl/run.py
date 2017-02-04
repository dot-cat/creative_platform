#!/usr/bin/env python

import logging

from dpl.core.controller import Controller

logger = logging.getLogger("dpl")
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    controller = Controller()
    controller.run_api()
