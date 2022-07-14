# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:09:30 2022

@author: Vikram
"""
#Enter no of panels
import numpy as np
import scipy.integrate as integrate
import scipy as scipy
import matplotlib as mp
convergence=1
No_of_panel=1;
N_panel=No_of_panel-1;
#Enter distance from Robot arm as array in order[meters].
pi=np.pi;
#D=[1]
sigma=5.67*10**(-8)
#Enter Timestep for iteration
t=0.1;
i=0
#Enter Dimensions of Materials in Sequence([L,B],[L,B],...) Negligible thickness assumed
Dimensions=[[1,1]]

# Enter Material properties
# Material | Absorptivity, Emissivity, Heat Capacity (J/g K), Thermal Conductivity (W/m K), Density kg/m^3

  #  "Air": None,
M_p=[[0.27, 0.76, 0.9, 237, 2700]] 
M_p=[[0.25,0.88]] #Glass
#M_p=[[0.19,0.77]] #Alumium Backed Mylar, emergency blankets
#M_p=[[0.175,0.725]]#Glass Fiber
M_p=[[0.15,0.04]]# Al foil
 #   "Aluminium": [0.27, 0.76, 0.9, 237, 2700]  # Clear Anodized Aluminium
Area_emitting=[]
Area_absorption=[]
alpha=[]
epsilon=[]
T=[]
for i in range(0,N_panel+1):
     L=Dimensions[i][0]
     B=Dimensions[i][1]
     Area_emitting.append(L*B)
     Area_absorption.append(L*B)
     #Change Area here if want to include elements of different shapes
     
for i in range(0,N_panel+1):   
  alpha.append(M_p[i][0]) 
  epsilon.append(M_p[i][1])
  
T_robotarm=303
epsilon_robotarm=0.96;

#Calculate View Factor
r=0.075; #radius of robot arm
s=0.075;#distance from cyclinder center
t=0.3;#breadth of plate
l=0.15;#height of plate
R=r/l;
Z=s/r;
T2=t/r;
def y(x):
    return R**2 *( 1-Z**2 - T2**2 * x**2 )

def v(x):
    return (1/pow( (pow(Z,2) + pow(T2,2) * pow(x,2) * 0.25 ),0.5))

def integfun(x):
    return ((Z * pow(v(x),2))*( 1- (1/(pi))*(np.arccos( (1+y(x))/(1-y(x)) ) - (1/(2*R))*( ( pow((1-y(x)),2) +pow(4* pow(R,2) * np.arccos(v(x)*((1+y(x))/(1-y(x)))),0.5) ) + (1+y(x))* np.arcsin(v(x)) - ((np.pi)/2) * (1-y(x)) ) ) ))

integrated_value,integrated_error= integrate.quad(integfun,0,1)
F12=(T2/(2*np.pi))*integrated_value
 # Equilibrium Equation: Energy_in=Energy_out
 # epsilon*sigma*Area_emitting*(T^4)=alpha*Area_absorption*sigma*(T_robotarm^4)*epsilon_robot arm
T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (F12*T_robotarm**4) * (epsilon_robotarm/epsilon[i]) ) )**0.25)

#T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (T_robotarm**4) * (epsilon_robotarm/epsilon[i]) )/ (4*pi*(D[i]**2)) )**0.25)
print('The Equilibrium temperature of Panel '+str(i+1)+' is '+str(T[i])+' Kelvin')

for i in range(0,N_panel):
        T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (T[i]^4) * (epsilon[i-1]/epsilon[i]) )))
      
       # T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (T[i]^4) * (epsilon[i-1]/epsilon[i]) )/ (4*pi*(D[i-1]^2)) )^0.25)
        print('The Equilibrium temperature of Panel'+str(i+1)+'is '+str(T[i]))
              
        
#Convective heat transfer simulation. Considering room temperature of 22degree Celsius
T_conv=[]
T_room=295;
A=t*l*2;
h=2.5;
h_plot=[]
# Equilibrium Equation: Energy_in=Energy_out
# epsilon*sigma*Area_emitting*(T^4)=alpha*Area_absorption*sigma*(T_robotarm^4)*epsilon_robot arm+h*A*(T-T_room)
def convfun(x): 
    return -epsilon[i]*sigma*Area_emitting[i]*pow(x,4)+1373*0.89*alpha[i]*Area_absorption[i]+alpha[i]*F12*Area_absorption[i]*sigma*pow(T_robotarm,4)*epsilon_robotarm-h*A*(x-T_room)
while(h<=100):
    Temperature=scipy.optimize.fsolve(convfun,250)
    T_conv.append(Temperature)
    h_plot.append(h)
    h=h+1
    
h=5;
Temperature2=scipy.optimize.fsolve(convfun,250)    
print('The Equilibrium temperature of Panel is '+str(Temperature2))   

mp.pyplot.plot(h_plot,T_conv)

mp.pyplot.xlabel('h(W/m2K)')
mp.pyplot.ylabel('T(K)')
    
    

