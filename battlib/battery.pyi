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
