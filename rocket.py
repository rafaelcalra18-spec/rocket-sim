import numpy as np
import yaml
import matplotlib.pyplot as plt
with open("data/params.yaml") as f:
    params = yaml.safe_load(f)

#Parameters for the rocket simulation:
#{'m_dry': 50.0, 'm_prop': 11.2, 'd': 0.177,
#'rail_length': 12.0, 'rail_elevation': 84.0, 
#'rail_heading': 90.0, 'h_site': 0.0, 'g': 9.81}

#loads the data from the csv file, into a 2d array, skipping the first row (the header)
thrust_data = np.loadtxt("data/thrust_curve.csv", delimiter=",", skiprows=1)
time_thrust = thrust_data[:,0]# breaks down the two arrays into 2 1d arrays, for easier use in the simulation
thrust_values = thrust_data[:,1]

cd_data = np.loadtxt("data/cd_mach.csv", delimiter=",", skiprows=1)
mach_values = cd_data[:,0]
drag_coefficent_values = cd_data[:,1]

#Interpolates the thrust points, to get a continuous function of thrust over time
def thrust(t):
    return np.interp(t, time_thrust, thrust_values)

#Interpolates the mach points, to get a continuous function of drag coefficient over time
#this is valid if the rocket stays bellow mach = 2
def drag_coefficient(mach):
    return np.interp(mach, mach_values, drag_coefficent_values)

I_total = np.trapezoid(thrust_values, time_thrust) #integrates the thrust curve to get the total impulse of the motor

exhaust_speed = I_total / params['m_prop'] #calculates the exhaust speed of the propelant relative to the rocket (assuming it's constant)

#Calculates the mass flow rate of th rocket in kg/s
def mdot(t):
    return -thrust(t)/exhaust_speed

if __name__ == "__main__":

    print("Total Impulse: ", I_total, "N.s")
    print("Exit Velocity: ", exhaust_speed, "m/s")

    #Plots the thrust curve and the drag coefficient curve
    plt.figure()
    plt.subplot(3,1,1)
    plt.plot(time_thrust, thrust_values)
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.grid()

    plt.subplot(3,1,2)
    plt.plot(mach_values, drag_coefficent_values)
    plt.xlabel("Mach Number")
    plt.ylabel("Drag Coefficient")
    plt.grid()

    plt.subplot(3,1,3)
    plt.plot(time_thrust, mdot(time_thrust))
    plt.xlabel("Time (s)")
    plt.ylabel("Mass flow rate (kg/s)")
    plt.grid()

    plt.tight_layout()
    plt.show()
