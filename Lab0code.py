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


'''Plotting simulation data along other data.'''
sim_V_dcp = [
    0,
    0.132653061224489998704,
    0.265306122448979997408,
    0.397959183673469996112,
    0.530612244897959994816,
    0.6632653061224500490312,
    0.795918367346939992224,
    0.9285714285714299354169,
    1.061224489795919989632,
    1.1938775510204100438472,
    1.3265306122449000980623,
    1.4591836734693899302329,
    1.591836734693879984448,
    1.7244897959183700386632,
    1.8571428571428598708337,
    1.9897959183673499250489,
    2.122448979591839979264,
    2.2551020408163298114346,
    2.3877551020408200876943,
    2.5204081632653099198649,
    2.6530612244898001961246,
    2.7857142857142900282952,
    2.9183673469387798604657,
    3.0510204081632701367255,
    3.183673469387759968896,
    3.3163265306122498010666,
    3.4489795918367400773263,
    3.5816326530612299094969,
    3.7142857142857197416674,
    3.8469387755102100179272,
    3.9795918367346998500977,
    4.1122448979591901263575,
    4.244897959183679958528,
    4.3775510204081697906986,
    4.5102040816326596228691,
    4.6428571428571503432181,
    4.7755102040816401753887,
    4.9081632653061300075592,
    5.0408163265306198397298,
    5.1734693877551096719003,
    5.3061224489796003922493,
    5.4387755102040902244198,
    5.5714285714285800565904,
    5.7040816326530698887609,
    5.8367346938775597209315,
    5.969387755102049553102,
    6.102040816326540273451,
    6.2346938775510301056215,
    6.3673469387755199377921,
    6.5000000000000097699626
]
sim_w_vals= [ 
    0,
    0, 
    0, 
    0, 
    0, 
    0, 
    0.0880472161294149208155, 
    0.3428123077455788592083, 
    0.5975773993617430335235, 
    0.8523424909779071523275, 
    1.1071075825940712711315, 
    1.3618726742102351678909, 
    1.6166377658263992866949, 
    1.871402857442563405499 , 
    2.1261679490587273022584, 
    2.380933040674891643107 , 
    2.6356981322910555398664, 
    2.8904632239072194366258, 
    3.1452283155233842215637, 
    3.3999934071395476742339, 
    3.6547584987557124591717, 
    3.9095235903718759118419, 
    4.1642886819880402526906, 
    4.4190537736042037053608, 
    4.6738188652203689343878, 
    4.9285839568365314988796, 
    5.1833490484526967279066, 
    5.4381141400688610687553, 
    5.6928792316850236332471, 
    5.9476443233011888622741, 
    6.2024094149173532031227, 
    6.4571745065335166557929, 
    6.7119395981496809966416, 
    6.9667046897658453374902, 
    7.2214697813820087901604, 
    7.4762348729981740191874, 
    7.7309999646143374718577, 
    7.9857650562305018127063, 
    8.2405301478466643771981, 
    8.4952952394628287180467, 
    8.7500603310789948352522, 
    9.0048254226951591761008, 
    9.2595905143113217405926, 
    9.5143556059274860814412, 
    9.7691206975436504222898, 
    10.023885789159812986782, 
    10.278650880775979103987, 
    10.533415972392143444836,
    10.788181064008306009327,
    11.042946155624470350176
]


assert(len(sim_w_vals)== len(sim_V_dcp))
Vdcp = [1.55, 1.98, 2.36, 2.68, 3.36, 3.8, 3.97, 4.49, 4.94, 5.26, 5.67, 6.14]
Vi = [0.043, 0.049, 0.047, 0.052, 0.052, 0.055, 0.058, 0.059, 0.064, 0.067, 0.07, 0.071]
fenc = [198, 305, 386, 526, 667, 806, 917, 1025, 1150, 1310, 1380, 1490]
table_V = np.array(Vdcp)
table_w = np.array([(2*np.pi * fenc[i] / 960) for i in range(len(fenc))])
sim_V = np.array(sim_V_dcp)
sim_w = np.array(sim_w_vals)

fig, ax = plt.subplots()
ax.scatter(table_w, table_V, color="red", label="Table Data")
ax.scatter(sim_w, sim_V, color="Green", label="Simulated data")
ax.set_xlabel("V_dc (Volts)")
ax.set_ylabel("w (rad/s)")
ax.set_title("w changes as V_dc grows")

plt.legend()
plt.show()

