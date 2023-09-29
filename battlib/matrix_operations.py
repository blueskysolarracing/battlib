import numpy as np
import math

def initializeMatrix_A():
    A[0] = 1.0
    A[4] = math.exp(-DELTA_T / (R_CT * C_CT))
    A[8] = math.exp(-DELTA_T / (R_D * C_D))
    
def initializeMatrix_B():
    B[0] = -COULOMB_ETA*DELTA_T/Q_CAP
    B[2] = 1 - math.exp(-DELTA_T/(R_CT * C_CT))
    B[4] = 1 - math.exp(-DELTA_T/(R_D*C_D))

def additionEKF(op1,op2,result, size, subtract):
    
    coefficient = 1.0 if subtract == 0 else -1.0
    
    rows = size[0]
    cols = size[1]
    
    for i in range(rows):
        for j in range(cols):
            result[i*cols + j] = op1[i*cols + j] + coefficient * op2[i*cols + j]
    
def multiplyEKF(op1,op2, result, op1_Dim, op2_Dim):
    
    r1,c1 = op1_Dim[0], op1_Dim[1]
    r2,c2 = op2_Dim[0], op2_Dim[1]
    
    #temporary variable
    entryVal = 0.0
    
    if c1 != r2:
        return 0 #matrix manipulation not possible
    
    for i in range(r1):
        for j in range(c2):
            for k in range(c1):
                entryVal += op1[i*c1+k] * op2[k*c2+j]
                
            result[i*c2 + j] = entryVal
            entryVal = 0.0
        
    return 1 #matrix manipulation successful
    
def transposeEKF(matrixIn, matrixOut, matrixIn_Dim):
    rows, cols = matrixIn_Dim[0], matrixIn_Dim[1]
    
    for i in range(rows):
        for j in range(cols):
            matrixOut[j*rows + i] = matrixIn[i*cols + j]
            
def createIdentityEKF(inBuffer, size):
    for i in range(size):
        for j in range(size):
            inBuffer[i*size + j] = 1.0 if i ==j else 0.0
    
def inverseEKF(matrixIn, matrixOut, dim):
    rows,cols = dim[0],dim[1]
    
    if rows!=cols:
        print("Matrix not square - can't compute inverse with this method...")
        return 0
    
    if rows == 1:
        matrixOut[0] = 1.0/ matrixIn[0]
        return 1 #inverse was computed for 1x1 matrix
    
    #create copy of the current input
    copyIn = matrixIn.copy()
    
    createIdentityEKF(matrixOut, rows)
    ratio = 0.0
    
    #Gaussian Elimination: create upper triangle matrix
    for j in range(cols-1):
        #iterate through lower triangle to cancel out all elements
        for i in range(j+1, rows):
            ratio = copyIn[i*cols + j]/copyIn[j*cols + j]
            for k in range(cols):
                copyIn[i*cols + k] -= copyIn[j*cols + k]*ratio
                matrixOut[i*cols + k] -= matrixOut[j*cols + k]*ratio
                
    #Jordan Elimination: create diagonal matrix
    for j in range(cols):
        for i in range(j+1, rows):
            ratio = copyIn[(cols - 1 - i)*cols+(cols - 1 - j)]/copyIn[(cols - 1 - j)*cols+(cols - 1 - j)]
            copyIn[(cols - 1 - i)*cols+(cols - 1 - j)] -= copyIn[(cols - 1 - j)*cols+(cols - 1 - j)] * ratio
            
            for k in range(cols):
                matrixOut[(cols - 1 - i)*cols+(cols - 1 - k)] -= matrixOut[(cols - 1 - j)*cols+(cols - 1 - k)] * ratio
                
    #normalization
    for i in range(rows):
        temp = copyIn[i*cols + i]
        copyIn[i*cols + 1] = 1
        
        for j in range(cols):
            matrixOut[i*cols + j] /= temp
    return 1
                
                
            

def compute_A_B_dt(dt):
    
    A[0] = 1.0
    A[4] = math.exp(-dt / (R_CT * C_CT))
    A[8] = math.exp(-dt / (R_D * C_D))
    
