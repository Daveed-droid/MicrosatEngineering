"""
@Project ：Microsat Engineering
@File ：Thermal_Simulation_B1.py
@Author ：David Canosa Ybarra
@Date ：02/06/2022 17:15
"""
from TS_Formulas import *
import numpy as np
from matplotlib import pyplot as plt

Robot_arm_spacing = 0.1  # Required distance from the robot arm

# Adding material properties
# Material | Absorptivity, Emissivity, Heat Capacity (J/g K), Thermal Conductivity (W/m K), Density kg/m^3
Material_lst = {
    "Air": None,
    "Glass": [0.28, 0.87, 0.84, 0.81, 2500],  # Opal Glass
    "Aluminium": [0.27, 0.76, 0.9, 237, 2700]  # Clear Anodized Aluminium
}


class Panel:
    def __init__(self, Material, Thickness):
        self.Material = Material
        self.Thickness = Thickness
        self.Temp_K = None

    def __str__(self):
        return f"{self.Material} panel, {self.Thickness} m  thick"


# Creating the robot arm cover
# The panel list starts with the panel closest to the heat source and builds towards the camera
class Assembly:
    def __init__(self, Panel_lst):
        self.Panel_lst = Panel_lst

    def __add__(self, other):
        self.Panel_lst = self.Panel_lst + other.Panel_lst

    def __str__(self):
        return f"{self.Panel_lst}"

    def set_up(self, room_temp_K = 294):
        # TODO: Combine gaps to one big gap
        # TODO: Check that it starts and ends with a gap
        for Panel in self.Panel_lst:
            Panel.Temp_K = room_temp_K

    def simulate(self, arm_temp_K, dt):

        Panel_Temp_K = [[]]
        Panel_Heat_C = [[]]
        Panel_Density = [[]]
        Panel_Thickness = [[]]
        for Panel_i in range(len(self.Panel_lst)):
            if self.Panel_lst[Panel_i].Material != "Air":
                Panel_Temp_K[0].append(self.Panel_lst[Panel_i].Temp_K)
                Panel_Heat_C[0].append(Material_lst[self.Panel_lst[Panel_i].Material][2] * 1000)  # in kg
                Panel_Density[0].append(Material_lst[self.Panel_lst[Panel_i].Material][4])  # in kg
                Panel_Thickness[0].append(self.Panel_lst[Panel_i].Thickness)
        Panel_Temp_K_ar = np.array(Panel_Temp_K)
        print(Panel_Heat_C)
        print(Panel_Temp_K_ar)
        changing = True
        T = [0]
        while changing:
            Q_em_lst = []
            Q_em_lst.append(Power_E(1, arm_temp_K))
            # Generate Power Emitted List
            for Panel in self.Panel_lst:
                if Panel.Material != "Air":
                    Q_em_lst.append(Power_E(1, Panel.Temp_K))
            Q_em_lst.append(0)
            print(f"Qemlst: {Q_em_lst}")
            Q_re_lst = []
            # Generate Power Received List
            Q_re_i = 0
            for Panel_i in range(len(self.Panel_lst)):
                if self.Panel_lst[Panel_i].Material != "Air":
                    Q_re_lst.append(Power_R(Q_em_lst[Panel_i - 1], 1, self.Panel_lst[Panel_i - 1].Thickness))
                    try:
                        Q_re_lst[Q_re_i] = Q_re_lst[Q_re_i] + Power_R(Q_em_lst[Panel_i + 1], 1,
                                                                      self.Panel_lst[Panel_i + 1].Thickness)
                    except IndexError:
                        pass
                    Q_re_i = Q_re_i + 1
            Q_re_ar = np.array(Q_re_lst)
            print(f"Qrelst: {Q_re_ar}")
            Panel_Heat_C_ar = np.array(Panel_Heat_C)
            Panel_Density_ar = np.array(Panel_Density)
            Panel_Thickness_ar = np.array(Panel_Thickness)
            Panel_Temp_K_ar_plusdt = Panel_Temp_K_ar[-1] + (Q_re_ar * dt + (
                    Panel_Temp_K_ar[-1] * Panel_Heat_C_ar * Panel_Density_ar * Panel_Thickness_ar * 1)) / (
                                             Panel_Heat_C_ar * Panel_Density_ar * Panel_Thickness_ar * 1)
            Panel_Temp_K_ar = np.vstack((Panel_Temp_K_ar, Panel_Temp_K_ar_plusdt))
            T.append(T[-1] + dt)
            print(f"{Panel_Temp_K_ar}\n{Panel_Temp_K_ar_plusdt}\n{Panel_Temp_K_ar[-1]}")
            changing = np.any(np.abs(Panel_Temp_K_ar[-2] - Panel_Temp_K_ar_plusdt) > 0.01)
            print(changing)
            print(np.abs(Panel_Temp_K_ar[-1] - Panel_Temp_K_ar_plusdt))
        plt.plot(T, Panel_Temp_K_ar[:, 0])
        plt.show()
        # TODO: Simulate 1 panel setup


Test = Assembly([
    Panel("Air", 0.1),
    Panel("Glass", 0.1),
    Panel("Air", 0.1),
    Panel("Aluminium", 0.2),
    Panel("Air", 0.1)
])
Test.set_up()
Test.simulate(300, 0.1)
