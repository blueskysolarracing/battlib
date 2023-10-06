import numpy as np
from battery_measurements import SOC, OCV

def initializeMatrix_A():
    A[0] = 1.0
    A[4] = math.exp(-DELTA_T / (R_CT * C_CT))
    A[8] = math.exp(-DELTA_T / (R_D * C_D))
    
def initializeMatrix_B():
    B[0] = -COULOMB_ETA*DELTA_T/Q_CAP
    B[2] = 1 - math.exp(-DELTA_T/(R_CT * C_CT))
    B[4] = 1 - math.exp(-DELTA_T/(R_D*C_D))
    
def compute_A_B_dt(dt):
    
    A[0] = 1.0
    A[4] = math.exp(-dt / (R_CT * C_CT))
    A[8] = math.exp(-dt / (R_D * C_D))

def initializeBatteryAlgo(inBatteryPack, initialV, initial_dT):
    
    for unit in range(NUM_14P_UNITS):
        initializeEKFModel(inBatteryPack.batteryPack[unit], initialV[unit])
        
    compute_A_B_dt(initial_dT)
    
def initializeEKFModel(inBattery, initialV):
    i,j = 0
    
    #initializes state variables
    for i in range(STATE_NUM):
        if i ==0:
            inBattery.stateX[i] = [SOC(initialV)]
        else:
            inBattery.stateX[i] = 0.0
            
    #initialize covariance matrix
    for i in range(STATE_NUM):
        for j in range(STATE_NUM):
            if i == j:
                inBattery.covP[i*STATE_NUM +j] = covList[i]
            else:
                inBattery.covP[i* STATE_NUM + j] = 0.0

def run_EKF(inputBatt, dt, currentIn, measuredV):
    #insert code for using APIs
   
    #calculate A and B matrices based on dt
    compute_A_B_dt(dt)
   
    I_Input = currentIn  #current reading
    I_InSign = 0.0

    if I_Input != 0:
        I_InSign = 1.0 if I_Input > 0.0 else -1.0

    V_Measured[0] = measuredV  #voltage reading
    V_OCV[0] = OCV(inputBatt.stateX[0])
   
    #compute the a priori state covariance
    A_T = np.transpose(A)
    A_P = np.dot(A, inputBatt.covP)
    A_P_AT = np.dot(A_P, A_T)
    P_k1 = A_P_AT + Q

    #compute the a priori state covariance
    C_T = np.transpose(C)
    C_P = np.dot(C, P_k1)
    C_P_CT = np.dot(C_P, C_T)
    S = C_P_CT + R
   
    #compute Kalman Gain
    SInv = np.linalg.inv(S)
    P_CT = np.dot(P_k1, C_T)
    W = np.dot(P_CT, SInv)
   
    #update Posteriori covariance
    W_T = np.transpose(W)
    W_S = np.dot(W, S)
    W_S_WT = np.dot(W_S, W_T)
    inputBatt.covP = P_k1 + W_S_WT
   
    #A priori state estimate
    A_X = np.dot(A, inputBatt.stateX)
    B_U = np.dot(B, U)
    X_k1 = A_X + B_U
   
    #A priori measurement
    C_X = np.dot(C, X_k1)
    D_U = np.dot(D, U)
    CX_DU = C_X + D_U
    Z_k1 = V_OCV + CX_DU
   
    #update of posteriori state estimate
    Z_err = V_Measured + Z_k1
    W_Zerr = np.dot(W, Z_err)
    inputBatt.stateX = X_k1 + W_Zerr  #SOC in inputBatt.stateX[0]
       
