""":mod:`battlib.battery` implements the battery coulomb counting algorithm.
"""

import numpy as np


class CCSOCEstimator:
    """The class for the battery coulomb counting algorithm for battery
    state of charge estimation.

    :param battery: The battery model.
    :param initial_voltage: The initial voltage of the battery.
    """

    def __init__(self, battery, initial_voltage):
        self.battery = battery
        self.soc = battery.interp_soc(initial_voltage)

    def step(self, i_in, dt):
        """Perform a single step prediction and update using the battery
        coulomb counting algorithm

        :param i_in: Input Current (in amperes).
        :param dt: Time step (in seconds).
        :return: ``None``.
        """
        dq = -i_in * dt
        self.soc += dq / self.battery.q_cap
        self.soc = np.clip(self.soc, 0, 1)
