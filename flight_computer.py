import numpy as np
from rocket import params, drag_coefficient   # nominal yaml values + the Cd table
from atmosphere import isa                    # density at the current altitude


# Takes the estimated apogee, calulates error, runs PID and gives back the deployment to the airbrake
def pid(state, t, deployment_cmd, acumulated_error, previous_error, estimated_deployment, dt):
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
        m_dry = params['m_dry']
        target = 2750

        # this tells the computer where the flaps are: it starts from its own previous estimate
        # and moves it towards the last command, at most 2.0/s over one tick (two Euler steps of dt)
        max_move = 2 * 2*dt
        deployment_necesary = deployment_cmd - estimated_deployment
        if deployment_necesary >= max_move:
            estimated_deployment = estimated_deployment + max_move
        elif deployment_necesary <= -max_move:
            estimated_deployment = estimated_deployment - max_move
        else: # if in the middle the flaps reach the command
            estimated_deployment = deployment_cmd
        actual_deployment = estimated_deployment

        # apogee calculation
        k = (rho/(2*m_dry))*(Cd_airbrake * Area_airbrake * actual_deployment + Cd_ship*Area_ship)
        hmax = (1/(2*k)) * np.log((9.81 + vz**2 *k)/9.81) + z # equation for apogee height, derived in notebook

        # Error calculation
        error = hmax - target # convention, needing to break more implies a positive error

        # PID
        Kp = 0.0004 # proportional term, tuned by grid search on 9 rockets (mass and drag +-10%)

        # anti_windup
        if deployment_cmd == 0 and error < 0 or deployment_cmd == 1 and error > 0:
            acumulated_error = acumulated_error # this line doesn't do much but it shows the antiwindup
        else:
            # The 2 behind dt accounts for the 50Hz
            acumulated_error += error* 2*dt # updates (integral from t to t+dt) the previous acumulated error (inputed by main)

        Ki = 0.03 # integral term, tuned by grid search on 9 rockets (mass and drag +-10%)

        derivative = (error - previous_error)/dt
        Kd = 0.0 # D did not help in the grid search

        deployment = Kp * error + Ki * acumulated_error + Kd * derivative
        deployment = np.clip(deployment, 0, 1) # cliping the output to what the actuator takes in [0,1]

        return deployment, acumulated_error, error, estimated_deployment



