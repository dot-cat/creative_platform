from dpl.core.things import AbsSlider
from dpl.specific.things.shift_reg.slider import Slider, ShiftRegBuffered


def get_slider_by_params(con_instance, con_params, metadata=None) -> AbsSlider:
    if isinstance(con_instance, ShiftRegBuffered):
        return Slider(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Slider for specified connection is missing")
