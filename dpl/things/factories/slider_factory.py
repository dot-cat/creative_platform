from dpl.things.specific.shift_reg.slider import AbsSlider, Slider, ShiftRegBuffered


def get_slider_by_params(con_instance, con_params, metadata=None) -> AbsSlider:
    if isinstance(con_instance, ShiftRegBuffered):
        return Slider(con_instance, con_params, metadata)

    else:
        raise ValueError("Implementation of Slider for specified connection is missing")
