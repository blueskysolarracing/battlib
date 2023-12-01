.. battlib documentation master file, created by
   sphinx-quickstart on Wed Sep 13 00:31:48 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to battlib's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Version History:

Overview:
   This library contains a set of modules that can be used to calculate the state of charge of a battery.

Package contents:

1. init.py

This module is the entry point of the battlib library. It is the top-level package that gathers the tools for battery modeling and state estimation. The __all__ attribute lists modules considered public (Battery, BatteryEKF, intexterp).

2. battery.py

This file contains a ‘battery’ class that is used for modeling a battery with specific physical properties and variance parameters, including the essential characteristics of a battery (open circuit voltage, state of charge). The class provides methods for interpolating state of charge (SOC) based on the open circuit voltage (OCV) (using the interp_soc method) and interpolating the OCV based on the SOC (using the intexterp_ocv method).   

—----Example Usage—----

i) To create an instance of the Battery class:

new_battery = Battery(
ocv = np.array[2.0, 2.5, 3.5], 
soc = np.array[20,40,80], 
q_cap = 2250,
 r_int = 0.01,
 r_ct = 0.1,
 c_ct = 80,
 r_d = 0.06,
 c_d = 50,
 var_z = 0.02,
 var_i_ct = 0.002,
 var_i_d = 0.0002,
 var_sens = 0.0002,
 var_in = 0.00002,
 coulomb_eta = 0.80 )

ii) To interpolate SOC from OCV:

ocv = 4.7
interpolated_soc = new_battery.interp_soc(ocv)

iii) To interpolate OCV from SOC:

soc = 80
interpolated_ocv = new_battery.intexterp_ocv(soc)

3. battery_ekf.py

This file contains a BatteryEKF class that estimates the state of charge (SOC) of a battery by implementing the Extended Kalman Filter (EKF) algorithm.

—----Example Usage—----

An instance of the Battery class must be made before using the methods in the class BatteryEKF. Refer to section 2) i).

i) To create an instance of the BatteryEKF class:

initial_voltage = 5.0
new_battery_ekf = BatteryEKF(new_battery, intiial_voltage)

ii) To perform a single step prediction and update using the BatteryEKF

time_step = 1.0
current_in = 3.0
measured_voltage = 4.3
new_battery_ekf.step(time_step, current_in, measured_voltage)

iii) To access the estimated state of charge (SOC)

estimated_soc = new_battery_ekf.soc

4. utilities.py

This file contains a method for interpolating/extrapolating sample data.

—----Example Usage—----

x_vals = [1, 2, 3]
y_vals = [20, 30, 40]
interpolated _val = intexterp(2.5, x_vals, y_vals) 

Dependencies:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
