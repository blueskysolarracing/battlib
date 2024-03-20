from battlib.battery import Battery, SOCEstimator


class OCVSOCEstimator(SOCEstimator):
    soc: float

    def __init__(self, battery: Battery, initial_voltage: float) -> None: ...
    def step(self, *, dt: float | None = None, i_in: float | None = None, measured_v: float) -> None: ...
