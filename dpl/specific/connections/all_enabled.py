##############################################################################################
# FIXME List:
# CC20 - Consider Change 20
#   Этот файл нужен только для того, чтобы вызвать принудительный импорт соединений
#   и, как следствие, заставить их зарегистрироваться в ConnectionRegister
##############################################################################################

# FIXME: CC20
from .mpd_client import MPDClientConnection
from .shift_reg_gpio_buffered import ShiftRegGPIOBuffered

__all__ = ['MPDClientConnection', 'ShiftRegGPIOBuffered']
