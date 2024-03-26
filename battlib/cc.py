""":mod:`battlib.battery` implements the battery coulomb counting algorithm.
"""

import numpy as np

from battlib.battery import SOCEstimator


class CCSOCEstimator(SOCEstimator):
    """The class for the battery coulomb counting algorithm for battery
    state of charge estimation.

    :param battery: The battery model.
    :param initial_voltage: The initial voltage of the battery.
    """

    def __init__(self, battery, initial_voltage):
        self.battery = battery
        self.soc = battery.interp_soc(initial_voltage)
        self.soc_errors = []

    def step(self, *, dt, i_in, measured_v=None, actual_soc=None):
        dq = -i_in * dt
        self.soc += dq / self.battery.q_cap
        self.soc = np.clip(self.soc, 0, 1)

        if actual_soc:
            soc_error = actual_soc - self.soc
            self.soc_errors.append(soc_error)

    def rms_calculation(self):
        soc_errors_squared = np.square(self.soc_errors)
        rms = np.sqrt(np.mean(soc_errors_squared))
        return rms
