import numpy as np
from rocket import params, drag_coefficient   # nominal yaml values + the Cd table
from atmosphere import isa                    # density at the current altitude


# Takes the estimated apogee, calulates error, runs PID and gives back the deployment to the airbrake
def pid(state, t):
    if t < 5.5:
        deployment = 0 
    else: 
        x, y, z, vx, vy, vz, m = state[0], state[1], state[2], state[3], state[4], state[5], state[6]
        P, T, rho, speed_sound = isa(z)
        
