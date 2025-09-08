import matplotlib.pyplot as plt
import numpy as np

''' Part 1 : line of best fit for 0.B.2 '''
# Finding R_m
V_dcp = [0.57, 1.5, 2.12, 3.06, 4.12, 4.92, 6.43]
V_I = [0.04, 0.101, 0.136, 0.195, 0.250, 0.289, 0.344]
#VDC = R_m(I_dc) when the motor is still (this is because Vemf is dependent on w, and L_m is negligible)
#VDC is also not just VDCp. It is Vdcp - Vi
R_I = 1/6
def calculateRm(Vi, Vdcp, Ri):  
    Idc = Vi / Ri # current through the Ri resistor = current through motor
    Rm = (Vdcp-Vi) / Idc
    return Rm



R_m_values = [calculateRm(V_I[i], V_dcp[i], R_I) for i in range(len(V_dcp))]

#Average of the R_m values 
# print(sum(R_m_values) / len(R_m_values))

V_dc = np.array([V_dcp[i] - V_I[i] for i in range(len(V_dcp))])
I_dc = np.array([V_I[i] / R_I for i in range(len(V_I))])

Rms = [V_dc[i] / I_dc[i] for i in range(len(V_dc))]
slope, intercept = np.polyfit(I_dc, V_dc, 1) # creates a model for the line of best fit of the scatter plot
linear_fit = slope * I_dc + intercept

#plot settings
# print("slope of line: ", slope) # this number is higher than just the average Rm values... interesting.
# fig, ax = plt.subplots()
# ax.scatter(I_dc, V_dc, label="data")
# ax.plot(I_dc, linear_fit, color="red", linestyle="dashed")
# ax.set_xlabel("I_dc (Amps)")
# ax.set_ylabel("V_dc (Volts)")
# ax.set_title("Linear fit of I_dc vs V_dc")
# plt.show()



''' Part 2: finding k, B, and Tint'''

# finding k, B, and T_int

# w = (2pi/ 960 )* fenc
# Tload = Tint + Text (assume Text = 0)

Vdc = [1.55, 1.98, 2.36, 2.68, 3.36, 3.8, 3.97, 4.49, 4.94, 5.26, 5.67, 6.14]
Vi = [0.043, 0.049, 0.047, 0.052, 0.052, 0.055, 0.058, 0.059, 0.064, 0.067, 0.07, 0.071]
fenc = [198, 305, 386, 526, 667, 806, 917, 1025, 1150, 1310, 1380, 1490]

V_emf = [Vdc[i] - (Vi[i]/R_I) - Vi[i] for i in range(len(Vdc))]
w_vals = [(2*np.pi * fenc[i] / 960) for i in range(len(fenc))]
w = np.array(w_vals)
k = np.array([V_emf[i] / w_vals[i]] for i in range(len(V_emf)))

slope, intercept = np.polyfit(w, k, 1) # creates a model for the line of best fit of the scatter plot
linear_fit = slope * w + intercept

#plot settings
fig, ax = plt.subplots()
ax.scatter(w, k, label="data")
ax.plot(w, linear_fit, color="red", linestyle="dashed")
ax.set_xlabel("w (radians/sec)")
ax.set_ylabel("k")
ax.set_title("Linear fit of k vs w (to find average k)")
plt.show()