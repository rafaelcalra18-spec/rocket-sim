import numpy as np
from rocket import thrust,  drag_coefficient, mdot, params
from aero import drag_force
from atmosphere import isa

def derivative(t, state, deployment): 
    theta = np.radians(params['rail_elevation'])   # 84 -> 1.466
    psi = np.radians(params['rail_heading'])       # 90 -> 1.571

    # components of the direction of the rail, dependent on theta and psi
    rail_x = np.sin(psi) * np.cos(theta)
    rail_y = np.cos(psi) * np.cos(theta)
    rail_z = np.sin(theta)
    rail_direction = np.array([rail_x, rail_y, rail_z])
    rail = rail_direction * params['rail_length'] # rail vector in space

    vx, vy, vz = state[3], state[4], state[5] # take the velocities of the state at t
    v = np.array([vx, vy, vz]) # turn that into one vector for drag_force
    mod_v = np.linalg.norm(v)  # scalar of velocity
    position = np.array([state[0], state[1], state[2]])

    m = state[6] # take the mass at t 
    h = state[2] + params['h_site'] # height above sea level
    g = np.array([0, 0, - params['g']]) # vector of weight (in this case the 1/m removes m)
    P, T, rho, speed_sound = isa(h) # take all the atmospheric data from ISA

    # This is all the parameters of the actuator beeing controled
    Cd_airbrake = 2.0
    Area_airbrake = 0.02
    drag_airbrakes = 0.5 * rho * mod_v**2 * Cd_airbrake * Area_airbrake * deployment  

    # This is the phase of the rocket in the rail
    if np.dot(position, rail_direction) < params['rail_length']: # valid till it's off the rail
        if thrust(t) <= params['g']* m * np.sin(theta): # this simulated the rail's normal force till thrust overtakes the weight
            a = np.array([0, 0, 0]) 
        else:
            mod_drag = np.linalg.norm(drag_force(v, rho, speed_sound))
            a = (1/m * (thrust(t) - mod_drag) - params['g'] * np.sin(theta)) * rail_direction # once it actually is accelerating

    else:
        d = np.array([vx, vy, vz]) / mod_v # create the direction vector (used in unconstrained motion)
        drag_total = drag_force(v, rho, speed_sound) + drag_airbrakes * d
        a = 1/m * (thrust(t)*d - drag_total) + g # equation of motion in the air (off the rail)
    
    ax, ay, az = a[0], a[1], a[2]

    return np.array([vx, vy, vz, ax, ay, az, mdot(t)])

if __name__ == '__main__':
    ###############_____test____####################
    #t = 0 with s = [0, 0, 0, 0, 0, 0, 61.2]
    #t = 1.0 with s = [0, 0, 0, 0, 0, 0, 61.2]
    #t = 10.0, s = [100, 0, 2000, 50, 0, 0, 50.0]
    #right before leaving the rail
    #right after leaving the rail 

    print(derivative(0, [0, 0, 0, 0, 0, 0, 61.2])) 

    print(derivative(1, [0, 0, 0, 0, 0, 0, 61.2]))

    print(derivative(10, [100, 0, 2000, 50, 0, 0, 50.0]))

    print(derivative(1.0, [1.25330, 0, 11.92432, 3.13585, 0, 29.83566, 60.0]))

    print(derivative(1.0, [1.25539, 0, 11.94421, 3.13585, 0, 29.83566, 60.0]))
    #all of the above work !!!