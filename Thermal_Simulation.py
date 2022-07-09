"""
@Project ：Microsat Engineering
@File ：Thermal_Simulation.py
@Author ：David Canosa Ybarra
@Date ：02/06/2022 17:15
"""
from TS_Formulas import *

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


# Creating the robot arm cover
# The panel list starts with the panel closest to the heat source and builds towards the camera
class Assembly:
    def __init__(self, Panel_lst):
        self.Panel_lst = Panel_lst

    def __add__(self, other):
        self.Panel_lst = self.Panel_lst + other.Panel_lst

    def set_up(self, room_temp_K = 294):
        # TODO: Combine gaps to one big gap
        # TODO: Check that it starts and ends with a gap
        for Panel in self.Panel_lst:
            Panel.Temp_K = room_temp_K

    def simulate(self, arm_temp_K):
        Q_em = Power_E(1, arm_temp_K)
        Q_em_lst = []
        Q_em_lst.append(Power_E(1, arm_temp_K))
        # Generate Power Emitted List
        for Panel in self.Panel_lst:
            if Panel.Material != "Air":
                Q_em_lst.append(Power_E(1, Panel.Temp_K))
        Q_em_lst.append(0)
        Q_re_lst = []
        panel_count = 0
        # Generate Power Received List
        for Panel in self.Panel_lst:

            if Panel.Material != "Air":
                Q_re_lst.append(Power_R(Q_em_lst(Q_em_lst[panel_count], 1, )))
            if len(self.Panel_lst) > 1:
                if Panel == self.Panel_lst[1]:

                elif Panel == self.Panel_lst[-2]:
                    pass
                else:
                    pass
            else:
            # TODO: Simulate 1 panel setup
            panel_count = panel_count + 1


Test = Assembly([
    Panel("Air", 0.1),
    Panel("Glass", 0.1),
    Panel("Air", 0.1),
    Panel("Aluminium", 0.2),
    Panel("Air", 0.1)
])
