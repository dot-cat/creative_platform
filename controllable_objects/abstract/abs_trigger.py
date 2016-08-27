from controllable_objects.abstract.abs_controllable import AbsControllable


class AbsTrigger(AbsControllable):
    """
    Объект с двумя состояниями: включено и выключено
    """

    def __init__(self, con_instance, con_params):
        """
        Конструктор, копия конструктора из базового класса
        """
        super().__init__(con_instance, con_params)

    def set_on(self):
        """
        Немедленно устанавливает триггер в состояние "включено"
        """
        self.set_state(self.States.on)

    def set_off(self):
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        self.set_state(self.States.off)

    def toggle(self):
        """
        Переключить из текущего состояния в противоположное
        """
        if self.get_state() == self.States.on:  # если переключатель включен
            # выключаем его
            self.set_off()

        else:  # если переключатель выключен...
            # включаем его
            self.set_on()
