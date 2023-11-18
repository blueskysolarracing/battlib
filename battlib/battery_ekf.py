from filterpy.kalman import ExtendedKalmanFilter
import numpy as np


class BatteryEKF(ExtendedKalmanFilter):
    """The class for battery EKF algorithm."""

    DIM_X = 3
    """The number of state variables."""
    DIM_Z = 1
    """The number of measurement inputs."""

    def __init__(self, battery, initial_voltage):
        super().__init__(self.DIM_X, self.DIM_Z)

        self.battery = battery
        self.x = np.array([battery.interp_soc(initial_voltage), 0, 0])
        self.P = np.diag([battery.var_z, battery.var_i_ct, battery.var_i_d])
        self.R = np.atleast_2d(battery.var_sens)
        self.Q = np.eye(self.DIM_X) * battery.var_in
        self.HJacobian = np.atleast_2d([0, -battery.r_ct, -battery.r_d])
        self.D = np.atleast_2d([-battery.r_int, 0])

    @property
    def soc(self):
        return self.x[0]

    def step(self, dt, i_in, measured_v):
        self.B = np.array(
            [
                [-self.battery.coulomb_eta * dt / self.battery.q_cap, 0],
                [
                    1.0 - np.exp(-dt / (self.battery.r_ct * self.battery.c_ct)),
                    0,
                ],
                [1.0 - np.exp(-dt / (self.battery.r_d * self.battery.c_d)), 0],
            ]
        )
        self.F = np.diag(
            [
                1.0,
                np.exp(-dt / (self.battery.r_ct * self.battery.c_ct)),
                np.exp(-dt / (self.battery.r_d * self.battery.c_d)),
            ],
        )
        u = np.array([i_in, np.sign(i_in)]).T

        self.predict_update(
            measured_v,
            lambda *_: self.HJacobian,
            lambda x, *_: (
                self.battery.intexterp_ocv(x[0]) + self.HJacobian @ x + self.D @ u
            ),
            u=u,
        )
