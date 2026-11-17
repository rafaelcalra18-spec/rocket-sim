"""Animation of the flight from main.py: side view of the trajectory, with the rocket moving along it."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from main import times, brute_states
from rocket import params, time_thrust
from atmosphere import isa

SAVE_GIF = False      # set to True to also write flight.gif
STEPS_PER_FRAME = 10  # 10 steps of 0.01 s = 0.1 s of flight per frame
ROCKET_LENGTH = 120   # drawn length of the rocket in metres (not to scale, so it is visible)

t = np.array(times)
s = np.array(brute_states)
x, y, z = s[:, 0], s[:, 1], s[:, 2]
v = s[:, 3:6]
speed = np.linalg.norm(v, axis=1)
mach = speed / isa(z + params['h_site'])[3]
horizontal = np.hypot(x, y)
burnout = time_thrust[-1]

theta = np.radians(params['rail_elevation'])
psi = np.radians(params['rail_heading'])
rail_dir = np.array([np.sin(psi) * np.cos(theta), np.cos(psi) * np.cos(theta), np.sin(theta)])
along_rail = s[:, 0:3] @ rail_dir

def phase(i):
    if along_rail[i] < params['rail_length']:
        return "on the rail"
    if t[i] < burnout:
        return "powered flight"
    return "coasting"

fig = plt.figure(figsize=(12, 8))
grid = fig.add_gridspec(3, 2, width_ratios=[1, 1.4], height_ratios=[0.8, 1, 1])
ax = fig.add_subplot(grid[:, 0])          # side view of the trajectory
ax_info = fig.add_subplot(grid[0, 1])     # live numbers
ax_alt = fig.add_subplot(grid[1, 1])      # altitude against time
ax_spd = fig.add_subplot(grid[2, 1], sharex=ax_alt)  # speed against time

ax.plot(horizontal, z, color="0.85", linewidth=1, linestyle="--")  # full path, faint
trail, = ax.plot([], [], color="tab:blue", linewidth=2)
body, = ax.plot([], [], color="black", linewidth=4, solid_capstyle="round")
flame, = ax.plot([], [], color="tab:orange", linewidth=6, solid_capstyle="round")

ax.set_aspect("equal")
ax.set_xlim(-150, horizontal.max() + 150)
ax.set_ylim(-50, z.max() + 150)
ax.set_xlabel("Horizontal distance from the pad (m)")
ax.set_ylabel("Altitude (m)")
ax.set_title("Flight to apogee (side view)")

ax_info.axis("off")
info = ax_info.text(0.0, 1.0, "", va="top", family="monospace", fontsize=12)

ax_alt.plot(t, z, color="0.85", linewidth=1, linestyle="--")
alt_line, = ax_alt.plot([], [], color="tab:blue", linewidth=2)
alt_dot, = ax_alt.plot([], [], "o", color="tab:blue")
ax_alt.set_ylabel("Altitude (m)")

ax_spd.plot(t, speed, color="0.85", linewidth=1, linestyle="--")
spd_line, = ax_spd.plot([], [], color="tab:red", linewidth=2)
spd_dot, = ax_spd.plot([], [], "o", color="tab:red")
ax_spd.set_ylabel("Speed (m/s)")
ax_spd.set_xlabel("Time (s)")

for a in (ax, ax_alt, ax_spd):
    a.grid(alpha=0.3)
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
for a in (ax_alt, ax_spd):
    a.axvline(burnout, color="tab:orange", linewidth=1, linestyle=":")
ax_spd.text(burnout, speed.max() * 0.05, " burnout", color="tab:orange", fontsize=9)
plt.setp(ax_alt.get_xticklabels(), visible=False)
fig.tight_layout()

frames = range(0, len(t), STEPS_PER_FRAME)

def update(i):
    trail.set_data(horizontal[:i + 1], z[:i + 1])

    # rocket body drawn along the velocity (or the rail before it moves)
    if speed[i] > 0:
        direction = np.array([np.hypot(v[i, 0], v[i, 1]), v[i, 2]]) / speed[i]
    else:
        direction = np.array([np.hypot(rail_dir[0], rail_dir[1]), rail_dir[2]])
    nose = np.array([horizontal[i], z[i]])
    tail = nose - ROCKET_LENGTH * direction
    body.set_data([tail[0], nose[0]], [tail[1], nose[1]])

    if t[i] < burnout:
        flame_end = tail - 0.5 * ROCKET_LENGTH * direction
        flame.set_data([flame_end[0], tail[0]], [flame_end[1], tail[1]])
    else:
        flame.set_data([], [])

    alt_line.set_data(t[:i + 1], z[:i + 1])
    alt_dot.set_data([t[i]], [z[i]])
    spd_line.set_data(t[:i + 1], speed[:i + 1])
    spd_dot.set_data([t[i]], [speed[i]])

    info.set_text(f"t        {t[i]:6.1f} s\n"
                  f"altitude {z[i]:6.0f} m\n"
                  f"speed    {speed[i]:6.0f} m/s\n"
                  f"Mach     {mach[i]:6.2f}\n"
                  f"mass     {s[i, 6]:6.1f} kg\n"
                  f"{phase(i)}")
    return trail, body, flame, info, alt_line, alt_dot, spd_line, spd_dot

anim = FuncAnimation(fig, update, frames=frames, interval=33, blit=False, repeat=False)

if SAVE_GIF:
    anim.save("flight.gif", writer=PillowWriter(fps=30))

plt.show()
