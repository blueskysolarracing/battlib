import math
import numpy as np

# BSSR_OCV, BSSR_SOC

def calculate_SOC(ocv):
    """
    Calculate the state of charge (soc) of battery based on open circuit voltage (ocv) using linear interpolation.
    
    Use binary search to find appropriate range of ocv values, will then use to calculate change in soc and change in ocv
    
    Perform linear interpolation to estimate soc for given ocv
    """
    dsoc, docv, soc = 0.0
    
    #for very low voltages
    if ocv<= BSSR_OCV[0]:
        soc = 0
        return soc
    #for very high voltages
    elif ocv >= BSSR_OCV[LUT_SIZE-1]:
        soc = 1
        return soc
    #if ocv falls within range of boundary points
    elif (ocv > BSSR_OCV[0]) and ocv < BSSR_OCV[LUT_SIZE -1]: #can use len instead?
        
        #perform binary search
        low = 0
        high = LUT_SIZE - 1
        
        while low <= high:
            mid = (low + high)//2
            
            #range found
            if ocv >= BSSR_OCV[mid] and ocv < BSSR_OCV[mid+ 1]:
                low = mid
                #calculating change in soc/ocv
                dsoc = BSSR_SOC[low + 1] - BSSR_SOC[low]
                docv = BSSR_OCV[low + 1] - BSSR_OCV[low]
                
                #calculating soc
                soc = (ocv - BSSR_OCV[low])* (dsoc/docv) + BSSR_SOC[low]
                return soc
            
            #below middle
            elif ocv < BSSR_OCV[mid]:
                high = mid -1
            #above middle
            else:
                low = mid + 1   
    else:
        return 0
    
def calculate_OCV (soc):
    
    # initializing change in voltage and ocv
    dv, ocv = 0.0
    dsoc = BSSR_SOC[1] - BSSR_SOC[0]
    
    #using method of linear interpolation
    if soc <= BSSR_SOC[0]:
        dv = BSSR_OCV[1] - BSSR_OCV[0]
        ocv = (soc - BSSR_SOC[0]) * (dv/dsoc) + BSSR_OCV[0]
        return ocv
    elif soc >= BSSR_SOC[LUT_SIZE - 1]:
        dv - BSSR_OCV[LUT_SIZE - 1] - BSSR_OCV[LUT_SIZE - 2]
        ocv = (soc - BSSR_SOC[LUT_SIZE-1])*(dv/dsoc)+BSSR_OCV[LUT_SIZE-1]
        return ocv
    elif BSSR_SOC[0] < soc < BSSR_SOC[LUT_SIZE - 1]:
        lowerIndex = int((soc - BSSR_SOC[0])/dsoc)
        dv = BSSR_OCV[lowerIndex+1]-BSSR_OCV[lowerIndex]
        ocv = BSSR_OCV[lowerIndex] + ((soc - BSSR_SOC[lowerIndex])*(dv/dsoc))
        return ocv
    else:
        return 0.0
    
    #checking if soc val less than or equal to lowesr SOC val in BSSR_SOC
    
    
                
        
         
        
        