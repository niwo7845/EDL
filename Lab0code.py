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
print(sum(R_m_values) / len(R_m_values))
# output 2.513764525079611

V_dc = np.array([V_dcp[i] - V_I[i] for i in range(len(V_dcp))])
I_dc = np.array([V_I[i] / R_I for i in range(len(V_I))])

Rms = [V_dc[i] / I_dc[i] for i in range(len(V_dc))]
slope, intercept = np.polyfit(I_dc, V_dc, 1) # creates a model for the line of best fit of the scatter plot
linear_fit = slope * I_dc + intercept

#plot settings
print("slope (R_m): ", slope) # this number is higher than just the average Rm values... interesting.
# # output: slope of line:  2.971048259215362
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

Vdcp = [1.55, 1.98, 2.36, 2.68, 3.36, 3.8, 3.97, 4.49, 4.94, 5.26, 5.67, 6.14]
Vi = [0.043, 0.049, 0.047, 0.052, 0.052, 0.055, 0.058, 0.059, 0.064, 0.067, 0.07, 0.071]
fenc = [198, 305, 386, 526, 667, 806, 917, 1025, 1150, 1310, 1380, 1490]
R_m = slope


# Vi / Ri = Idc 
V_emf = [float(Vdcp[i] - ((Vi[i]*R_m/R_I)+Vi[i]) ) for i in range(len(Vdcp))]
w_vals = [(2*np.pi * fenc[i] / 960) for i in range(len(fenc))]
w = np.array(w_vals)
k = np.array([V_emf[i] / w_vals[i] for i in range(len(V_emf))])

slope, intercept = np.polyfit(w, V_emf, 1) # creates a model for the line of best fit of the scatter plot
linear_fit = slope * w + intercept
print("slope (k-value):", slope)
k = slope
# output: slope (k-value): 0.46337067122057407

# k output
# plot settings
# fig, ax = plt.subplots()
# ax.scatter(w, V_emf, label="data")
# ax.plot(w, linear_fit, color="red", linestyle="dashed")
# ax.set_xlabel("w (radians/sec)")
# ax.set_ylabel("V_emf (Volts)")
# ax.set_title("Linear fit of V_emf vs w (to find average k)")
# plt.show()


# finding B and Tint

# T = J(dw/dt) + Bw + Tload
# in this case Tload = Tint because it is a free spinning motor with no external torque
# also, dw/dt = 0 because the motor is spinning at a constant speed
# so the new equation is T = Bw + Tint
# this is a simple line mx+b style linear equation
# k * I_dc = Bw + Tint

T = [k * Vi[i] / R_I for i in range(len(Vi))] # essentially k * I_dc for each of the points
# we already have an w array from above. 

slope, intercept = np.polyfit(w, T, 1) # creates a model for the line of best fit of the scatter plot
linear_fit = slope * w + intercept
# in this case, slope should be B, and Tint should be w
B = slope
Tint = intercept
print("B:",B)
print("Tint:",Tint)

# fig, ax = plt.subplots()
# ax.scatter(w, T, label="data")
# ax.plot(w, linear_fit, color="red", linestyle="dashed")
# ax.set_xlabel("w (radians/sec)")
# ax.set_ylabel("T (N*m)")
# ax.set_title("Linear fit of T vs w (to find Tint and B)")
# plt.show()


'''Part 3: solving for J using diff eq'''
# i wrote down my thoughts in comments for this part. 
# w(t) = Ke^(-Bt/J) - Tint/B
# using the previously determined values for Tint and B, we can start to solve the equation. first of all, fenc = 1490. 
# this means that w = (2pi / 960 ) * 1490. 
w_full_speed = np.pi * 2 * 1490 / 960
# also, the initial V_dc of the solution (after the drop off) is about 5 V (this is at w(0))
V_dc_init = 5
# and, the delay until the motor loses all of its speed, tau, is 3.4 s
tau = 3.4
# since Tint and B are constants, not depending on the motor speed, we can determine their value. We will call this z for now
z = Tint/ B
# now, at a time tau after the motor has been running, the w value = 0 making the equation: 
# w(tau) = 0 = (w_full_speed + z)e^(-B(tau)/J) - z
# this can be rearranged: 
# z /(w_full_speed + z) = e ^ (-B(tau)/J) (we are going to rename the left side to "left")
left = z / (w_full_speed + z)
# ln(left) = -B(tau)/J
# J = -B(tau)/ln(left)
J= -1*B*(tau)/(np.log(left)) # np.log is actually an ln function : https://stackoverflow.com/questions/10593100/how-do-you-do-natural-logs-e-g-ln-with-numpy-in-python -> i checked this by doing np.log(np.e)
print(J)