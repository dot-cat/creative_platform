from dpl.libs.shift_reg_buffered import ShiftRegBuffered

from dpl.core.connections import Connection, ConnectionFactory
from dpl.core.connections import ConnectionRegistry
from dpl.libs.shift_reg_gpio import ShiftRegGPIO


class ShiftRegGPIOBuffered(ShiftRegBuffered, Connection):
    def __init__(self, con_params: dict):
        Connection.__init__(self)
        ShiftRegBuffered.__init__(
            self
            , ShiftRegGPIO(**con_params)
        )


class ShiftRegGPIOBufferedFactory(ConnectionFactory):
    @staticmethod
    def build(config: dict) -> ShiftRegGPIOBuffered:
        return ShiftRegGPIOBuffered(
            config["con_params"]
        )


ConnectionRegistry.register_factory(
    "shift_reg",
    ShiftRegGPIOBufferedFactory()
)
