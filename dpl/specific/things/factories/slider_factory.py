from dpl.core.things import Slider
from dpl.specific.things.shift_reg.slider import ShiftRegSlider, ShiftRegBuffered


def get_slider_by_params(con_instance, con_params, metadata=None) -> Slider:
    if isinstance(con_instance, ShiftRegBuffered):
        return ShiftRegSlider(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Slider for specified connection is missing")
