""":mod:`battlib.battery` contains tools to define the battery
characteristics.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np

from battlib.utilities import intexterp


@dataclass
class Battery:
    """The class for the model of the battery. This class is designed as
    a ``dataclass`` to contain all the battery parameters.
    """

    # open circuit voltage curve

    ocv: np.ndarray
    """Open circuit voltages, from the lowest to the highest."""
    soc: np.ndarray
    """State of charges, from zero to a hundred percent."""

    # physical properties

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

    # variances

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
        """Interpolate the state of charge (SOC) based on the provided
        open circuit voltage (OCV).

        :param ocv: The ocv.
        :return: The soc.
        """
        return np.interp(ocv, self.ocv, self.soc)

    def intexterp_ocv(self, soc):
        """Interpolate the open circuit voltage (OCV) based on the
        provided state of charge (SOC).

        :param soc: The SOC.
        :return: The OCV.
        """
        return intexterp(soc, self.soc, self.ocv)


class SOCEstimator(ABC):
    """The class for the battery state-of-charge (SOC) estimator."""

    battery: Battery
    """The battery being estimated."""
    soc: float
    """The battery state-of-charge (SOC)."""

    @abstractmethod
    def step(self, *, dt, i_in, measured_v):
        """Perform a single step prediction and update.

        :param dt: Time step (in seconds).
        :param i_in: Input current (in amperes).
        :param measured_v: Measured voltage (in volts).
        :return: ``None``.
        """
        pass
