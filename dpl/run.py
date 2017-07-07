#!/usr/bin/env python

import logging
import argparse

from dpl.core.controller import Controller

logger = logging.getLogger("dpl")
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="a custom path to config files")

    args = parser.parse_args()  # type: argparse.Namespace

    if args.config is not None:
        controller = Controller(args.config)
    else:
        controller = Controller()

    controller.run_api()
    controller.disable_all_things()
