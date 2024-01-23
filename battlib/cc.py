""":mod:`battlib.battery` implements the battery coulomb counting algorithm.
"""


class BatteryCC:
    """The class for the battery coulomb counting algorithm for
    battery state of charge estimation."""

    def __init__(self, battery, initial_soc):
        self.battery = battery
        self.SOC = initial_soc

    @property
    def soc(self):
        """Return the state of charge (SOC) of the battery.

        :return: The battery soc.
        """
        return self.SOC

    def step(self, i_in, dt, measured_v=None):
        """Perform a single step prediction and update using the battery
        coulomb counting algorithm

        :param i_in: Input Current (in amperes).
        :param dt: Time step (in seconds).
        :return: ``None``.
        """
        dq = -i_in * dt
        self.SOC += dq/self.battery.q_cap

        # ensuring that soc stays within possible range
        if self.SOC < 0:
            self.SOC = 0
        elif self.SOC > 1:
            self.SOC = 1
