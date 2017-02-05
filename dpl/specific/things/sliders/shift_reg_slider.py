##############################################################################################
# FIXME List:
# CC3 - Consider Change 3
#   См. файл things/specific/shift_reg_trigger.py
# CC4 - Consider Change 4
#   Проверка на тип толком и не нужна: наличие полей pos, neg и их типы проверяются и так.
# CC5 - Consider Change 5
#   Вместо количества секунд передавать функцию, которая будет ждать окончания перехода.
# CC6 - Consider Change 6
#   Защита на случай многопоточного выполнения - предотвращает зависание двери в не-
#   определенном состоянии (например, предотвращает останов двери раньше времени).
##############################################################################################

from dpl.core.things import Slider, ThingRegistry, ThingFactory, Actuator
from dpl.specific.connections.shift_reg_gpio_buffered import ShiftRegBuffered, ShiftRegGPIOBuffered


def check_shift_reg_type(test_obj):
    if not isinstance(test_obj, ShiftRegBuffered):
        raise ValueError('type of con_instance value must be a ShiftRegBuffered')


class ShiftRegSlider(Slider):
    """
    Объект с четырьмя состояниями: закрыто, открывается, открыто, открывается.
    connections'ом выступает сдвиговый регистр
    """
    class ConParams(object):
        """
        Структура (почти), содержит информацию, необходимую для работы со сдвиговым регистром.
        """
        def __init__(self, pin_pos, pin_neg, transition_time=1):
            """
            Конструктор
            :param pin_pos: положительный пин на сдвиговом регистре
            :param pin_neg: отрицательный пин на сдвиговом регистре
            :param transition_time: время переключения между состояниями в секундах
            """
            if pin_pos == pin_neg:
                raise ValueError('pos and neg pins can\'t be the same')

            if transition_time <= 0:
                raise ValueError('transition_time must be bigger than zero')

            self.pos = pin_pos
            self.neg = pin_neg
            self.transition_time = transition_time  # Fixme: CC5

    def __init__(self, con_instance, con_params: ConParams or dict, metadata=None):
        """
        Конструктор
        :param metadata:
        :param con_instance: экземпляр сдвигового регистра
        :param con_params: заполненная структура self.ConParams, информация о подключении.
               Или словарь, на основе которого такую структуру можно создать.
        """
        check_shift_reg_type(con_instance)

        con_params_error = ValueError(
            "con_params must be an instance of "
            "Slider.ConParams class or a compatible dict"
        )

        if not isinstance(con_params, self.ConParams):  # Fixme: CC4
            if isinstance(con_params, dict):
                try:
                    con_params = self.ConParams(**con_params)
                except TypeError:
                    raise con_params_error
            else:
                raise con_params_error

        con_instance.check_bit_pos(con_params.pos)  # Fixme: CC3
        con_instance.check_bit_pos(con_params.neg)  # Fixme: CC3

        super().__init__(con_instance, con_params, metadata)

        self.close()  # Закрываем дверь, если она была открыта

    @property
    def state(self) -> Slider.States:
        """
        Текущее состояние объекта
        :return: объект типа self.States
        """
        raise NotImplementedError

    @property
    def is_available(self) -> bool:
        """
        Доступность объекта для использования
        :return: True - доступен, False - недоступен
        """
        raise NotImplementedError

    @property
    def last_seen(self) -> float:
        """
        Возвращает время, когда объект был доступен в последний раз
        :return: float, UNIX time
        """
        raise NotImplementedError

    def disable(self) -> None:
        """
        Отключает объект, останавливает обновление состояния и
        делает его неактивным
        :return: None
        """
        raise NotImplementedError

    def enable(self) -> None:
        """
        Включает объект, запускает обновление состояние и делает
        его активным
        :return: None
        """
        raise NotImplementedError

    def open(self) -> Actuator.ExecutionResult:
        """
        Открывает слайдер
        :return: Actuator.ExecutionResult
        """
        raise NotImplementedError

    def close(self) -> Actuator.ExecutionResult:
        """
        Закрывает слайдер
        :return: Actuator.ExecutionResult
        """
        raise NotImplementedError


class ShiftRegSliderFactory(ThingFactory):
    @staticmethod
    def build(con_instance: ShiftRegBuffered, con_params: dict, metadata: dict=None) -> ShiftRegSlider:
        cp = ShiftRegSlider.ConParams(**con_params)
        return ShiftRegSlider(con_instance, cp, metadata)


ThingRegistry.register_factory(
    "sunblind",
    ShiftRegGPIOBuffered,
    ShiftRegSliderFactory()
)

ThingRegistry.register_factory(
    "door",
    ShiftRegGPIOBuffered,
    ShiftRegSliderFactory()
)
