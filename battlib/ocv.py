""":mod:`battlib.battery` contains tools to define the battery
characteristics.
"""

from dataclasses import dataclass


@dataclass
class OCVSOCEstimator:
    """The class for the battery coulomb counting algorithm for
    battery state of charge estimation.

    :param battery: The battery model.
    :param initial_voltage: The initial voltage of the battery.
    """

    def __init__(self, battery, initial_voltage):
        self.battery = battery
        self.soc = battery.interp_soc(initial_voltage)

    def step(self, measured_v):
        """Perform a single step prediction and update using the battery
        extended Kalman filter (EKF) algorithm.

        :param measured_v: Measured voltage (in volts).
        :return: ``None``.
        """
        self.soc = self.battery.interp_soc(measured_v)
