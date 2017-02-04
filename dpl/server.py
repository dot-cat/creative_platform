#!/usr/bin/env python

import logging

logging.basicConfig(level=logging.DEBUG)

from dpl.controller import Controller


if __name__ == "__main__":
    controller = Controller()
    controller.start_api()
