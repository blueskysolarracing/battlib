from dataclasses import dataclass
import numpy as np

from battlib.utilities import intexterp


@dataclass
class Battery:
    """The class for battery modelling. This class is designed as a data class to simplify data storage/retrieval"""

    ocv: np.ndarray
    """Open circuit voltages, from the lowest to the highest."""
    soc: np.ndarray
    """State of charges, from zero to a hundred percent."""
    
    
    """Physical Properties:"""
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
    
    """Variance parameters:"""
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
    """Interpolates the state of charge (SOC) based on the provided open circuit voltage (OCV)"""

    def intexterp_ocv(self, soc):
        return intexterp(soc, self.soc, self.ocv)
    """Interpolates the open circuit voltage (OCV) based on the provided state of charge (SOC)"""
