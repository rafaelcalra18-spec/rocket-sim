import numpy as np
from rocket import thrust,  drag_coefficient, mdot, params
from aero import drag_force
from atmosphere import isa

def derivative(t, state): 

    vx, vy, vz = state[3], state[4], state[5] # take the velocities of the state at t
    v = np.array([vx, vy, vz]) # turn that into one vector for drag_force
    m = state[6] # take the mass at t 
    h = state[2] + params['h_site'] # height above sea level
    mod_v = np.sqrt(vx**2 +vy**2 + vz**2)  # scalar of velocity
    g = np.array([0, 0, - params['g']]) # vector of weight (in this case the 1/m removes m)
    P, T, rho, speed_sound = isa(h) # take all the atmospheric data from ISA
    d = np.array([vx, vy, vz]) / mod_v # create the direction vector (used for Thrust and Drag)

    a = 1/m * (thrust(t)*d + drag_force(v, rho, speed_sound)) + g # equation of motion
    ax, ay, az = a[0], a[1], a[2]

    return np.array([vx, vy, vz, ax, ay, az, mdot(t)])

print(derivative(2.0, [40, 0, 500, 18, 0, 169, 57.0]))