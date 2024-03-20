""":mod:`battlib.battery` implements the battery extended Kalman filter
(EKF) algorithm.
"""

from filterpy.kalman import ExtendedKalmanFilter
import numpy as np

from battlib.battery import SOCEstimator


class EKFSOCEstimator(ExtendedKalmanFilter, SOCEstimator):
    """The class for the battery extended Kalman filter (EKF) algorithm
    for battery state of charge estimation.

    :param battery: The battery model.
    :param initial_voltage: The initial voltage of the battery.
    """

    DIM_X = 3
    """The number of state variables."""
    DIM_Z = 1
    """The number of measurement inputs."""

    def __init__(self, battery, initial_voltage):
        super().__init__(self.DIM_X, self.DIM_Z)

        self.battery = battery
        """The battery model."""
        self.x = np.array([battery.interp_soc(initial_voltage), 0, 0])
        """State vector representing battery state (including SOC)."""
        self.P = np.diag([battery.var_z, battery.var_i_ct, battery.var_i_d])
        """Covariance matrix of the state vector (x)."""
        self.R = np.atleast_2d(battery.var_sens)
        """Covariance matrix of measurement noise."""
        self.Q = np.eye(self.DIM_X) * battery.var_in
        """Covariance matrix of process noise."""
        self.HJacobian = np.atleast_2d([0, -battery.r_ct, -battery.r_d])
        """Jacobian matrix used in the prediction step."""
        self.D = np.atleast_2d([-battery.r_int, 0])
        """Matrix used in prediction step of algorithm to incorporate
        external influences or inputs into the state prediction
        (battery's internal resistance).
        """

    @property
    def soc(self):
        """Return the state of charge (SOC) of the battery.

        :return: The battery soc.
        """
        return self.x[0]

    def step(self, *, dt, i_in, measured_v):
        q_cap = self.battery.q_cap
        r_ct = self.battery.r_ct
        c_ct = self.battery.c_ct
        r_d = self.battery.r_d
        c_d = self.battery.c_d
        coulomb_eta = self.battery.coulomb_eta
        self.B = np.array(
            [
                [-coulomb_eta * dt / q_cap, 0],
                [1.0 - np.exp(-dt / (r_ct * c_ct)), 0],
                [1.0 - np.exp(-dt / (r_d * c_d)), 0],
            ]
        )
        self.F = np.diag(
            [1.0, np.exp(-dt / (r_ct * c_ct)), np.exp(-dt / (r_d * c_d))],
        )
        u = np.array([i_in, np.sign(i_in)]).T

        self.predict_update(
            measured_v,
            lambda *_: self.HJacobian,
            lambda x, *_: (
                self.battery.intexterp_ocv(x[0])
                + self.HJacobian @ x
                + self.D @ u
            ),
            u=u,
        )
