from filterpy.kalman import ExtendedKalmanFilter  # type: ignore[import]
import numpy as np
import numpy.typing as npt

from battlib.battery import Battery

class EKFSOCEstimator(ExtendedKalmanFilter):  # type: ignore[misc]
    DIM_X: int
    DIM_Z: int
    battery: Battery
    x: npt.NDArray[np.float64]
    P: npt.NDArray[np.float64]
    R: npt.NDArray[np.float64]
    Q: npt.NDArray[np.float64]
    HJacobian: npt.NDArray[np.float64]
    D: npt.NDArray[np.float64]

    def __init__(self, battery: Battery, initial_voltage: float) -> None: ...
    @property
    def soc(self) -> float: ...
    def step(self, dt: int | float, i_in: float, measured_v: float) -> None: ...
