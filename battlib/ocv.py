""":mod:`battlib.battery` contains tools to define the battery
characteristics.
"""

from dataclasses import dataclass

from battlib.battery import SOCEstimator


@dataclass
class OCVSOCEstimator(SOCEstimator):
    """The class for the battery coulomb counting algorithm for
    battery state of charge estimation.

    :param battery: The battery model.
    :param initial_voltage: The initial voltage of the battery.
    """

    def __init__(self, battery, initial_voltage):
        self.battery = battery
        self.soc = battery.interp_soc(initial_voltage)

    def step(self, *, dt=None, i_in=None, measured_v):
        self.soc = self.battery.interp_soc(measured_v)
