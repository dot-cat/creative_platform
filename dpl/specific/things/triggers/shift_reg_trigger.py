##############################################################################################
# FIXME List:
# DH2 - Dirty Hack 2
#   Копипаста docstrings методов между классами. Возможно, docstrings в классах тоже
#   можно наследовать?
# CC3 - Consider Change 3
#   Номер пина проверяется несколько раз: один раз в конструкторе Trigger'а и каждый раз
#   при запуске метода set_buf_bit сдвигового регистра. Лишние потери производительности
#   на пустом месте
# CC22 - Consider Change 22
#   У ShiftRegTrigger и ShiftRegSlider схожая логика. Особенно это касается обработки
#   is_available и is_enabled. Возможно, похожие куски следует выделить в отдельный
#   базовый класс и наследоваться от него
##############################################################################################

import time

from dpl.core.things import Trigger, ThingRegistry, ThingFactory, Actuator
from dpl.specific.connections.shift_reg_gpio_buffered import ShiftRegBuffered, ShiftRegGPIOBuffered


def check_shift_reg_type(test_obj):
    if not isinstance(test_obj, ShiftRegBuffered):
        raise ValueError('type of con_instance value must be a ShiftRegBuffered')


class ShiftRegTrigger(Trigger):
    """
    Объект с двумя состояниями: включено и выключено,
    connection'ом выступает сдвиговый регистр
    """

    def __init__(self, con_instance: ShiftRegBuffered, con_params: int, metadata=None):
        """
        Конструктор
        :param con_instance: экземпляр сдвигового регистра
        :param con_params: целое число, пин сдвигового регистра, на который подключен триггер
        :param metadata: метаданные (см. конструктор Thing)
        """
        check_shift_reg_type(con_instance)

        con_instance.check_bit_pos(con_params)  # Fixme: CC3

        super().__init__(con_instance, con_params, metadata)

        self._is_enabled = True
        self._last_upd = time.time()

    @property
    def state(self):
        # FIXME: DH2
        """
        Вернуть свое состояние внешнему миру из буфера
        :return: значение типа self.States
        """
        return self.States(self._con_instance.get_buf_bit(self._con_params))

    @property
    def is_available(self) -> bool:
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        return self._is_enabled

    def _update_last_upd(self):
        self._last_upd = time.time()

    @property
    def last_updated(self) -> float:
        """
        Возвращает время, когда объект был обновлен в последний раз
        :return: float, UNIX time
        """
        return self._last_upd

    def disable(self) -> None:
        """
        Отключает объект, останавливает обновление состояния и
        делает его неактивным
        :return: None
        """
        self._is_enabled = False

        if self.on_avail_update:
            self.on_avail_update(self, None)

    def enable(self) -> None:
        """
        Включает объект, запускает обновление состояние и делает
        его активным
        :return: None
        """
        self._is_enabled = True

        if self.on_avail_update:
            self.on_avail_update(self, None)

    def _set_state(self, target):
        self._con_instance.set_buf_bit(self._con_params, target.value)
        self._con_instance.write_buffer()

        self._update_last_upd()

        if self.on_update:
            self.on_update(self, None)

    def on(self) -> Actuator.ExecutionResult:
        if not self.is_available:
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE

        self._set_state(self.States.on)

        return Actuator.ExecutionResult.OK

    def off(self) -> Actuator.ExecutionResult:
        if not self.is_available:
            return Actuator.ExecutionResult.IGNORED_UNAVAILABLE

        self._set_state(self.States.off)

        return Actuator.ExecutionResult.OK


class ShiftRegSliderFactory(ThingFactory):
    @staticmethod
    def build(con_instance: ShiftRegBuffered, con_params: dict, metadata: dict=None) -> ShiftRegTrigger:
        return ShiftRegTrigger(
            con_instance,
            con_params["sr_pin"],
            metadata
        )


ThingRegistry.register_factory(
    "lighting",
    ShiftRegGPIOBuffered,
    ShiftRegSliderFactory()
)

ThingRegistry.register_factory(
    "fan",
    ShiftRegGPIOBuffered,
    ShiftRegSliderFactory()
)

