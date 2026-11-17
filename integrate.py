import numpy as np
from dynamics import derivative
from rocket import params

def Euler(derivative, t, state, dt):
    state = state + derivative(t, state)*dt
    t += dt
        
    return state, t

if __name__ == "__main__":
    def f(t, y):
        return -y

    for dt in [0.1, 0.01]:
        y, t = 1.0, 0.0
        for i in range(round(1 / dt)):
            y, t = Euler(f, t, y, dt)
        print(dt, y, np.exp(-1))