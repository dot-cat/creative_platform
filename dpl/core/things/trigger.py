##############################################################################################
# FIXME List:
# CC10 - Consider Change 10
#   Нет проверки текущего состояния: можно "включить" или "выключить" триггер дважды.
##############################################################################################

import logging

from dpl.core.things import Thing


class Trigger(Thing):
    """
    Объект с двумя состояниями: включено и выключено
    """

    def __init__(self, con_instance, con_params, metadata=None):
        """
        Конструктор, копия конструктора из базового класса
        :param metadata:
        """
        super().__init__(con_instance, con_params, metadata)

    def on(self):
        """
        Немедленно устанавливает триггер в состояние "включено"
        """
        self.set_state(self.States.on)  # CC10

    def off(self):
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        self.set_state(self.States.off)  # CC10

    def set_on(self):
        """
        Немедленно устанавливает триггер в состояние "включено"
        """
        logging.warning("'set_on' method is deprecated. Use 'on' method instead")
        self.on()

    def set_off(self):
        """
        Немедленно устанавливает триггер в состояние "выключено"
        """
        logging.warning("'set_off' method is deprecated. Use 'off' method instead")
        self.off()

    def toggle(self):
        """
        Переключить из текущего состояния в противоположное
        """
        if self.get_state() == self.States.on:  # если переключатель включен
            # выключаем его
            self.off()

        elif self.get_state() == self.States.off:  # если переключатель выключен...
            # включаем его
            self.on()

        else:
            logging.debug(
                "Unable to toggle %s object from %s state",
                self,
                self.get_state()
            )
