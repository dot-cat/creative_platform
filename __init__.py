##############################################################################################
# FIXME List:
# CC20 - Consider Change 20
#   Этот файл нужен только для того, чтобы вызвать принудительный импорт соединений и вещей
#   и, как следствие, заставить их зарегистрироваться в ConnectionRegistry и ThingRegistry
#   соответственно.
##############################################################################################

# FIXME: CC20

from .mpd import MPDClientConnection, MPDPlayer
from .shift_reg_gpio import ShiftRegGPIOBuffered, ShiftRegSlider, ShiftRegTrigger

__all__ = ["MPDClientConnection", "MPDPlayer", "ShiftRegGPIOBuffered", "ShiftRegSlider", "ShiftRegTrigger"]
