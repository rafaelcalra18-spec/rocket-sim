import numpy as np
from rocket import drag_coefficient, params
import matplotlib.pyplot as plt

# Reference area from the brief: A = pi d^2 / 4. Computed once, it never changes.
A_ref = np.pi * params["d"]**2 / 4  # m^2

def drag_force(v, rho, a):
    """Drag force vector (N) for velocity vector v (m/s), air density rho and speed of sound a."""
    v = np.asarray(v, dtype=float)
    speed = np.linalg.norm(v)  # m/s
    if speed == 0:
        return np.zeros(3)  # not moving: no drag, and no direction to divide by

    mach = speed / a
    Cd = drag_coefficient(mach)
    magnitude = 0.5 * rho * speed**2 * Cd * A_ref
    return magnitude * v / speed  # points against the velocity (v/speed is the unit direction vector)

if __name__ == '__main__':
    print("drag_force([0, 0, 100], 1.225, 340.3) =", drag_force([0, 0, 100], 1.225, 340.3))

    a = 340.3
    speeds = np.linspace(0, 2 * a, 200)  # up to Mach 2
    drag = [np.linalg.norm(drag_force([0, 0, s], 1.225, a)) for s in speeds]

    plt.plot(speeds / a, drag, linewidth=2)
    plt.xlabel("Mach number")
    plt.ylabel("Drag (N)")
    plt.title("Drag at sea level (rho = 1.225, a = 340.3)")
    plt.grid(alpha=0.3)
    plt.show()

