from abc import ABC

import numpy as np
import numpy.typing as npt


class Battery:
    ocv: npt.NDArray[np.float64]
    soc: npt.NDArray[np.float64]
    q_cap: float
    r_int: float
    r_ct: float
    c_ct: float
    r_d: float
    c_d: float
    var_z: float
    var_i_ct: float
    var_i_d: float
    var_sens: float
    var_in: float
    coulomb_eta: float

    def interp_soc(self, ocv: float) -> float: ...  
    def intexterp_ocv(self, soc: float) -> float: ...


class SOCEstimator(ABC):
    battery: Battery

    @property
    def soc(self) -> float: ...
    def step(self, *, dt: float, i_in: float, measured_v: float) -> None: ...
