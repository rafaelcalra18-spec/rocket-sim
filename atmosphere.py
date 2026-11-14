from numpy import sqrt, linspace
import matplotlib.pyplot as plt

#Constants
P0 = 101325 #Pascal
T0 = 288.15 #kelvin (15 celsius)
g = 9.81 # assumed constant
R = 287 #J/(kg·K)
k = 0.0065 # K/m (this is part of the ISA model) 
adiabatic_index = 1.4

# all the formulas and derivations are in my notes
#this assumes constant g, a linear temperature gradient, no variation in the 
#specific gas constant of R and I used the ideal gas laws
def isa(h):
    P = P0*((T0 - k*h)/T0)**(g/(R*k))
    T = T0 - k*h
    rho = (P0/(R*T0))*(1 - (k/T0)*h)**((g/(R*k))-1)
    speed_sound = sqrt((adiabatic_index*P)/rho)

    return P, T, rho, speed_sound

if __name__ == "__main__":
    h = linspace(0, 11000, 500)
    P, T, rho, a = isa(h)

    panels = [
        (T, "Temperature (K)", "tab:red"),
        (P / 1000, "Pressure (kPa)", "tab:blue"),
        (rho, "Density (kg/m³)", "tab:green"),
        (a, "Speed of sound (m/s)", "tab:purple"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    for ax, (values, label, colour) in zip(axes.flat, panels):
        ax.plot(h / 1000, values, color=colour, linewidth=2)
        ax.set_title(label)
        ax.set_xlabel("Altitude (km)")
        ax.set_xlim(0, 11)
        ax.grid(alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("International Standard Atmosphere, troposphere (0 to 11 km)")
    fig.tight_layout()
    plt.show()
