# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:38:40 2018

@author: Runze Liu
"""
import numpy as np
import matplotlib.pyplot as plt

#Version Statement
"""
First version of Green_Ampt Infiltration modeling [Green roof], No extra inflow
I, no weir outflow Q, evaporation E assumed 0. Constant rainfall intensity i. 
Runoff occurs at the bottom of soil. Recesstion period has not been included yet.
Initial infiltrated water depth should not exceed the soil's saturated water
depth.
"""

#Soil Type:Loamy sand
K=1.177 #Hydraulic conductivity (inch/hr)
SH=2.413 #Suction head φ (inch/hr)
P=0.437 #Porosity η [i.e.saturated water content (%)]
EP=0.401 #Effective porosity θ [i.e. Field Capacity (%)]
Depth=10 #thickness of soil layer (inch)
deltaP=P-0 #Water content deficit Δθ (assume initial soil moisture is 0)
FCD=EP*Depth #Filed capacity (inch)
STD=P*Depth #Filed capacity (inch)

#Rainfall input
i=2 #rainfall intensity (inch/hr)

#Initial condition 
D=0 #Initial ponded water depth D (inch)
F=0.5 #Initial infiltrated water depth F (inch)
R0=0 # Initial cumulative precipitation (inch)
q=0 #initial runoff from the bottom of soil(inch)

#iteration
T=12 #rainfall duration (hours)
delta_t=1 #time steps
#Period before reaching field capacity
data_rnof_infl=np.array([]) # dataset of accumulative runoff with infiltration 
                            # considered
R=R0
for t in np.linspace(1,T,np.int(T)):
    if F>=FCD: #whether soil reaches field capacity
        break
    R=R+i*delta_t #cumulative precipitation
    f=K*(1-deltaP+deltaP*(R+SH)/F) #Green-Ampt
    F=F+f*delta_t #cumulative infiltrated water depth
    if F>=R:
        F=R # cumulative infiltrated water depth cannot exceed cumulative 
            # precipitation
    q1=0 #no runoff during this period
    data_rnof_infl=np.append(data_rnof_infl,q1)
#Period after reaching field capacity
if F>=FCD:
    #Period after soil being saturated
    if F>=STD: #whether soil reaches saturated state
        R3=R
        F3=F
        q3=q1
        for t3 in np.linspace(t,T,np.int(T-t+1)):
            if F3>=STD:
                if F3>=R3:
                    F3=R3 
                D=R3-F3 #ponded water depth
                if D>=0:
                    q=K*(D+Depth)/Depth 
                else:
                    q=K #two alternative runoff rates during this period
                q3=q3+q*delta_t
            else:  
                if F3>=R3:
                    F3=R3
                q3=q3+f*delta_t
            R3=R3+i*delta_t
            if q3>R3:
                q3=R3
            f=K*(1-deltaP+deltaP*(R3+SH)/F3)
            F3=F3+f*delta_t
            data_rnof_infl=np.append(data_rnof_infl,q3)
    #Period after reaching field capacity but not saturated
    else:
        R2=R
        F2=F
        q2=q1
        for t2 in np.linspace(t,T,np.int(T-t)):
            R2=R2+i*delta_t
            f=K*(1-deltaP+deltaP*(R2+SH)/F2)
            F2=F2+f*delta_t
            if F2>=R2:
                F2=R2
            q2=q2+f*delta_t #cumulative runoff from bottom; runoff rate=infiltration
                            #rate during this period.
            if q2>R2:
                q2=R2
            data_rnof_infl=np.append(data_rnof_infl,q2)
        #Period after soil being saturated after reached field capacity
        if F2>=STD:
            R3=R2
            F3=F2
            q3=q2
            for t3 in np.linspace(t2,T,np.int(T-t2+1)):
                if F3>=STD:
                    if F3>=R3:
                        F3=R3 
                    D=R3-F3 #ponded water depth
                    if D>=0:
                        q=K*(D+Depth)/Depth 
                    else:
                        q=K #two alternative runoff rates during this period
                    q3=q3+q*delta_t
                else:  
                    if F3>=R3:
                        F3=R3
                    q3=q3+f*delta_t
                R3=R3+i*delta_t
                if q3>R3:
                    q3=R3
                f=K*(1-deltaP+deltaP*(R3+SH)/F3)
                F3=F3+f*delta_t
                data_rnof_infl=np.append(data_rnof_infl,q3)
                
#Runoff WITHOUT Infiltration
data_rnof=np.array([]) #dataset of cumulative runoff without infiltration.
R=R0
for t_R in np.linspace(1,T,np.int(T)):
    R=R+i*delta_t
    data_rnof=np.append(data_rnof,R)

#Plot
plt.plot(np.linspace(1,T,np.int(T)),data_rnof,label="Without Infiltration")
plt.plot(np.linspace(1,T,np.int(T)),data_rnof_infl,label="With Infiltration")    
plt.legend()
plt.xlabel("Rainfall Duration (hours)")
plt.ylabel("Runoff Depth (inches)")
plt.title("Green-Ampt Effects on Runoff")