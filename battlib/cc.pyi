from battlib.battery import Battery, SOCEstimator


class CCSOCEstimator(SOCEstimator):
    soc: float

    def __init__(self, battery: Battery, initial_voltage: float) -> None: ...
    def step(self, *, dt: float, i_in: float, measured_v: float | None = None) -> None: ...
