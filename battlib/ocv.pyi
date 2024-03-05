from battlib.battery import Battery


class OCVSOCEstimator: 
    battery: Battery
    soc: float

    def __init__(self, battery: Battery, initial_voltage: float) -> None: ...
    def step(self, measured_v: float) -> None: ...
