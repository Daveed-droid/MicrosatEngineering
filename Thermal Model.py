# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 17:09:30 2022

@author: vikra
"""

#Enter no of panels
import numpy as np;
import scipy.integrate as integrate
convergence=1
No_of_panel=1;
N_panel=No_of_panel-1;
#Enter distance from Robot arm as array in order[meters].
pi=np.pi;
#D=[1]

#Enter Timestep for iteration
t=0.1;
i=0
#Enter Dimensions of Materials in Sequence([L,B],[L,B],...) Negligible thickness assumed
Dimensions=[[1,1]]

# Enter Material properties
# Material | Absorptivity, Emissivity, Heat Capacity (J/g K), Thermal Conductivity (W/m K), Density kg/m^3

  #  "Air": None,
M_p = [[0.28, 0.87, 0.84, 0.81, 2500], [0.28, 0.87, 0.84, 0.81, 2500]]
 #   "Aluminium": [0.27, 0.76, 0.9, 237, 2700]  # Clear Anodized Aluminium
Area_emitting=[]
Area_absorption = []
alpha = []
epsilon = []
T = []
for i in range(0, N_panel + 1):
    L = Dimensions[i][0]
    B = Dimensions[i][1]
    Area_emitting.append(L * B)
    Area_absorption.append(L * B)
    # Change Area here if want to include elements of different shapes

for i in range(0, N_panel + 1):
    alpha.append(M_p[i][0])
    epsilon.append(M_p[i][1])

T_robotarm = 303
epsilon_robotarm = 0.8;
i = 0
# Calculate View Factor
r = 1;  # radius of robot arm
s = 1;  # distance from cyclinder center
t = 0.3;  # breadth of plate
l = 0.3;  # height of plate
R = r / l;
Z = s / r;
T = t / r;


# NEW BRANCH
def integfun(x):
    y = R ** 2 * (1 - Z ** 2 - T ** 2 * x ** 2)
    v = (1 / (Z ** 2 + T ** 2 * x ** 2 * 0.25) ** 0.5)
    return (Z * v ** 2) * (1 - (1 / np.pi) * (np.arccos((1 + y) / (1 - y)) - (1 / (2 * R)) * (
                ((1 - y) ** 2 + 4 * R ** 2 * np.arccos(v * ((1 + y) / (1 - y)))) ** 0.5 + (1 + y) * np.arcsin(v) - (
                    np.pi / 2) * (1 - y))))


# y=lambda x:R**2 *( 1-Z**2 - T**2 * x**2 )
# v=lambda x:(1/(Z**2 + T**2 * x**2 * 0.25 )**0.5)
# integfun=lambda x:(Z * v**2)*( 1- (1/np.pi)*(np.arccos( (1+y)/(1-y) ) -
#                                            (1/(2*R))*( ((1-y)**2 + 4* R**2 *
#                                                         np.arccos(v*((1+y)/(1-y))))**0.5  +
#                                         (1+y)* np.arcsin(v) - (np.pi/2) * (1-y) ) ) )
F12 = integrate.quad(integfun, 0, 1)
F12 = (T / 2 * np.pi) * F12  # FIXME: TypeError: can't multiply sequence by non-int of type 'float'
# Equilibrium Equation: Energy_in=Energy_out
# epsilon*sigma*Area_emitting*(T^4)=alpha*Area_absorption*sigma*(T_robotarm^4)*epsilon_robot arm/(4*pi*(D[i-1]^2))
T.append(((alpha[i] * (Area_absorption[i] / Area_emitting[i]) * (T_robotarm ** 4) * (
            epsilon_robotarm / epsilon[i]))) ** 0.25)

# T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (T_robotarm**4) * (epsilon_robotarm/epsilon[i]) )/ (4*pi*(D[i]**2)) )**0.25)
print('The Equilibrium temperature of Panel ' + str(i + 1) + ' is ' + str(T[i]) + ' Kelvin')

for i in range(0, N_panel):
    T.append(((alpha[i] * (Area_absorption[i] / Area_emitting[i]) * (T[i] ^ 4) * (epsilon[i - 1] / epsilon[i]))))

       # T.append(( ( alpha[i] * (Area_absorption[i]/Area_emitting[i]) * (T[i]^4) * (epsilon[i-1]/epsilon[i]) )/ (4*pi*(D[i-1]^2)) )^0.25)
        print('The Equilibrium temperature of Panel' + str(i+1) +'is ' + str(T[i]))
