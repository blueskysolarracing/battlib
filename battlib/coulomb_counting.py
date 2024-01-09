""":mod:`battlib.battery` implements the battery coulomb counting algorithm.
"""


class BatteryCC:
    """The class for the battery coulomb counting algorithm for
    battery state of charge estimation."""

    def __init__(self, battery):
        self.battery = battery
        self.soc = 0.0

    def step(self, i_in, dt):
        """Perform a single step prediction and update using the battery
        coulomb counting algorithm

        :param i_in: Input Current (in amperes).
        :param dt: Time step (in seconds).
        :return: ``None``.
        """
        dq = i_in * dt
        self.soc += dq/self.battery.q_cap

        # ensuring that soc stays within possible range
        if self.soc < 0:
            self.soc = 0
        elif self.soc > 1:
            self.soc = 1

    @property
    def get_soc(self):
        """Return the state of charge (SOC) of the battery.

        :return: The battery soc.
        """
        return self.soc
