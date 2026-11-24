import numpy as np
from rocket import params, drag_coefficient   # nominal yaml values + the Cd table
from atmosphere import isa                    # density at the current altitude


# Takes the estimated apogee, calulates error, runs PID and gives back the deployment to the airbrake
def pid(state, t, deployment):
    if t < 5.5:
        deployment = 0 
    else: 
        # constants
        x, y, z, vx, vy, vz = state[0], state[1], state[2], state[3], state[4], state[5]
        v_dot = np.linalg.norm(np.array([vx, vy, vz]))
        P, T, rho, speed_sound = isa(z) # for now we will take all of these to be constant (they aren't)
        Cd_airbrake = 2.0
        Cd_ship = drag_coefficient(v_dot/speed_sound)
        Area_airbrake = 0.02
        Area_ship = 0.02460
        m_dry = 50
        target = 2500

        # apogee calculation
        k = (rho/(2*m_dry))*(Cd_airbrake*Area_airbrake*deployment + Cd_ship*Area_ship)
        hmax = (1/(2*k)) * np.log((9.81 + vz**2 *k)/9.81) + z # equation for apogee height, derived in notebook

        # Error calculation
        Error = target - hmax

        # PID
        #bla bla bla math stuff