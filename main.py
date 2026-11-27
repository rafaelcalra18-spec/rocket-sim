from integrate import Euler
from dynamics import derivative
import matplotlib.pyplot as plt
from rocket import params
import numpy as np
from flight_computer import pid

t = 0 
path = []
brute_states = []
times = []
m_init = params['m_prop'] + params['m_dry']
state = np.array([0, 0, 0, 0, 0, 0, m_init])
steps = 0
deployment = 0 #only for first loop
deployment_cmd = 0 # last command from the flight computer, held between ticks
dt = 0.01
acumulated_error = 0

while state[5] >= 0 and steps < 100000 : # while vz is positive + safety feature

    # This adjusts the two frequencies 100Hz for truth and 50Hz for flight computer
    if steps % 2 == 0:
        open_tick = True
    else:
        open_tick = False

    state, t, deployment = Euler(derivative, t, state, dt, deployment) #Euler requires the whole function as an input, outputs two things
    position = np.array([state[0], state[1], state[2]])
    input_computer = np.array([state[0], state[1], state[2], state[3], state[4], state[5]])

    # deployment input every 2 ticks (when True)
    if steps > 550:
        if open_tick == True: # we only listen to the computer every 50Hz
            deployment_cmd, acumulated_error = pid(input_computer, t, deployment_cmd, acumulated_error, dt) # this updates the comand every two ticks
            deployment_necesary = deployment_cmd - deployment
            if deployment_necesary >= 2*dt: #maximum deployment capacity of actuator in dt
                deployment += 2*dt
            elif deployment_necesary <= -2*dt: #minimum deployment capacity of actuator in dt
                deployment += -2*dt 
            else: # if in the middle just add the change in deployment
                deployment += deployment_necesary

        else: 
            deployment_necesary = deployment_cmd - deployment # command of the previous tick
            if deployment_necesary >= 2*dt: #maximum deployment capacity of actuator in dt
                deployment += 2*dt
            elif deployment_necesary <= -2*dt: #minimum deployment capacity of actuator in dt
                deployment += -2*dt 
            else: # if in the middle just add the change in deployment
                deployment += deployment_necesary

    else: 
        deployment = 0 # fins stay shut before 5.5s

    steps += 1
    path.append(position)
    brute_states.append(state)
    times.append(t)

path = np.array(path)

print(max(path[:, 2]))



