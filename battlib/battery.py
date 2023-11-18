from dataclasses import dataclass
import numpy as np

from battlib.utilities import intexterp


@dataclass
class Battery:
    """The class for battery modelling."""

    ocv: np.ndarray
    """Open circuit voltages, from the lowest to the highest."""
    soc: np.ndarray
    """State of charges, from zero to a hundred percent."""
    q_cap: float
    """The charge capacity, in Ampere-seconds."""
    r_int: float
    """The internal resistance, in Ohms"""
    r_ct: float
    """The charge transfer resistance, in Ohms."""
    c_ct: float
    """The charge transfer capacitance, in Farads."""
    r_d: float
    """The diffusion resistance, in Ohms."""
    c_d: float
    """The diffusion capacitance, in Farads."""
    var_z: float
    """The state estimate variance, unitless."""
    var_i_ct: float
    """The charge transfer current variance, unitless."""
    var_i_d: float
    """The diffusion current variance, unitless."""
    var_sens: float
    """The sensor uncertainty, unitless."""
    var_in: float
    """The input uncertainty, unitless."""
    coulomb_eta: float
    """The coulombic efficiency of the battery."""

    def interp_soc(self, ocv):
        return np.interp(ocv, self.ocv, self.soc)

    def intexterp_ocv(self, soc):
        return intexterp(soc, self.soc, self.ocv)
