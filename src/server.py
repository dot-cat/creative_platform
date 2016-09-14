#!/usr/bin/env python

from time import sleep
import logging

from controller import Controller


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    controller = Controller()

    try:
        while(True):
            sleep(10)
            #print('test')
    except KeyboardInterrupt:
        pass

    print('Exited')
    pass
