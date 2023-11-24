from filterpy.kalman import ExtendedKalmanFilter
import numpy as np


class BatteryEKF(ExtendedKalmanFilter):
    """The 'BatteryEKF' class implements an Extended Kalman Filter (EKF) algorithm for battery state estimation."""

    DIM_X = 3
    """The number of state variables."""
    DIM_Z = 1
    """The number of measurement inputs."""

    def __init__(self, battery, initial_voltage):
        super().__init__(self.DIM_X, self.DIM_Z)

        self.battery = battery
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
        """Matrix used in prediction step of algorithm to incorporate external influences or inputs into the state prediction (battery's internal resistance)."""
    """ 
    Initializes the batteryEKF instance.
    Parameters:
        battery: An object representing the battery model.
        initial_voltage: Initial voltage of the battery.
    """
    
    @property
    def soc(self):
        return self.x[0]
    """ Returns the state of charge (SOC) of the battery."""

    def step(self, dt, i_in, measured_v):
        q_cap = self.battery.q_cap
        """Battery capacity."""
        r_ct = self.battery.r_ct
        """Charge transfer resistance."""
        c_ct = self.battery.c_ct
        """Charge transfer capacitance."""
        r_d = self.battery.r_d
        """Diffusion resistance."""
        c_d = self.battery.c_d
        """Diffusion capacitance."""
        coulomb_eta = self.battery.coulomb_eta
        """Coulombic efficiency."""
        
        self.B = np.array(
            [
                [-coulomb_eta * dt / q_cap, 0],
                [1.0 - np.exp(-dt / (r_ct * c_ct)), 0],
                [1.0 - np.exp(-dt / (r_d * c_d)), 0],
            ]
        )
        """Input matrix for the prediction step."""
        
        self.F = np.diag(
            [1.0, np.exp(-dt / (r_ct * c_ct)), np.exp(-dt / (r_d * c_d))],
        )
        """State transition matrix for prediction step."""
        
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
    """ 
    Performs a single step prediction and update using the Extended Kalman Filter.
    Parameters:
        dt: Time step.
        i_in: Input current.
        measured_v: Measured voltage.
    """
