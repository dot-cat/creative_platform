
from abc import ABCMeta, abstractmethod

class Listener(object):
    __metaclass__ = ABCMeta

    @abstractmethod

    def __init__ (self, controlling, tty, baudrate): pass

    def __del__(self): pass

    def __data_waiter(self): pass

    def __handler(self, event): pass