import numpy as np
import yaml
import matplotlib.pyplot as plt
with open("data/params.yaml") as f:
    params = yaml.safe_load(f)

#Parameters for the rocket simulation:
#{'m_dry': 50.0, 'm_prop': 11.2, 'd': 0.177,
#'rail_length': 12.0, 'rail_elevation': 84.0, 
#'rail_heading': 90.0, 'h_site': 0.0, 'g': 9.81}

#Interpolates the thrust points, to get a continuous function of thrust over time
def thrust(t):
    #loads the data from the csv file, into a 2d array, skipping the first row (the header)
    thrust_data = np.loadtxt("data/thrust_curve.csv", delimiter=",", skiprows=1)

    #breaks down the two arrays into 4 1d arrays, for easier use in the simulation
    time_thrust = thrust_data[:,0]
    thrust_values = thrust_data[:,1]
    
    return np.interp(t, time_thrust, thrust_values)

#Interpolates the mach points, to get a continuous function of drag coefficient over time
def drag_coefficient(mach):
    cd_data = np.loadtxt("data/cd_mach.csv", delimiter=",", skiprows=1)

    mach_values = cd_data[:,0]
    drag_coefficent_values = cd_data[:,1]

    return np.interp(mach, mach_values, drag_coefficent_values)
