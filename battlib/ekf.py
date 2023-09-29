import numpy as np
from battery_measurements import calculate_SOC

def initializeBatteryAlgo(inBatteryPack, initialV, initial_dT):
    
    for unit in range(NUM_14P_UNITS):
        initializeEKFModel(inBatteryPack.batteryPack[unit], initialV[unit])
        
    compute_A_B_dt(initial_dT)
    
def initializeEKFModel(inBattery, initialV):
    i,j = 0
    
    #initializes state variables
    for i in range(STATE_NUM):
        if i ==0:
            inBattery.stateX[i] = [calculate_SOC(initialV)]
        else:
            inBattery.stateX[i] = 0.0
            
    #initialize covariance matrix
    for i in range(STATE_NUM):
        for j in range(STATE_NUM):
            if i == j:
                inBattery.covP[i*STATE_NUM +j] = covList[i]
            else:
                inBattery.covP[i* STATE_NUM + j] = 0.0
    
def runEKF(inputBatt, dt, currentIn, measuredV):
