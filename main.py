from integrate import Euler
from dynamics import derivative
import matplotlib.pyplot as plt
from rocket import params
import numpy as np

t = 0 
path = []
brute_states = []
times = []
m_init = params['m_prop'] + params['m_dry']
state = np.array([0, 0, 0, 0, 0, 0, m_init])
steps = 0

while state[5] >= 0 and steps < 100000 : # while vz is positive + safety feature
    state, t = Euler(derivative, t, state, 0.01) #Euler requires the whole function as an input, outputs two things
    position = np.array([state[0], state[1], state[2]])
    steps += 1
    path.append(position)
    brute_states.append(state)
    times.append(t)

path = np.array(path)

print(max(path[:, 2]))


