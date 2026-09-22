import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

"""
Using PN Guidance Law, Follow the question instructions to:
    (a) See if intercept will occur
    (b) Plot xy-plane trajectories and target on same plot
    (c) Repeat but add lateral acceleration limit to interceptor
        (|V_m*Theta'| <= 15 * 9.81 m/s^2) [15 G's]
"""

##### Initialize #####
Vt = 300.0
Vm = 700.0

theta_t = np.deg2rad(0.0)
R0 = 2000.0
beta0 = np.deg2rad(30.0)

# State order: [xM, yM, xT, yT, theta]
z0 = [
    0.0,
    0.0,
    R0 * np.cos(beta0),
    R0 * np.sin(beta0),
    beta0  # PN problem specifies theta(0) = beta0
]

##### Required Launch Angle, Theta0 #####
Theta0 = np.degrees(np.asin((Vt / Vm) * np.sin(beta0))) # default 12.37 deg


##### Derivative Function #####
def dynamics(t, z, Vm, Vt, theta_t):
    xM, yM, xT, yT, Theta = z

    # Current velocity components
    xtDot = Vt * np.cos(theta_t)
    ytDot = Vt * np.sin(theta_t)

    xmDot = Vm * np.cos(Theta)
    ymDot = Vm * np.sin(Theta)

    # Current relative geometry
    dx = xT - xM
    dy = yT - yM

    R = np.hypot(dx, dy)

    # Relative velocity
    dxDot = xtDot - xmDot
    dyDot = ytDot - ymDot

    # LOS rate
    betaDot = (dx * dyDot - dy * dxDot) / (R ** 2)

    # PN Guidance
    thetaDot = 3 * betaDot

    a_lateral = Vm * thetaDot

    # Outputs
    a_lateral_g = a_lateral / 9.81

    derivatives =  [
        xmDot,
        ymDot,
        xtDot,
        ytDot,
        thetaDot
    ]

    return derivatives, a_lateral_g


def intercept_event(t, z, Vm, Vt, theta_t):
    xM, yM, xT, yT, theta = z

    R = np.hypot(xT - xM, yT - yM)

    return R - 1.0


def ode_function(t, z, Vm, Vt, theta_t):
    derivatives, _ = dynamics(t, z, Vm, Vt, theta_t)
    return derivatives


##### Solve IVP #####
intercept_event.terminal = True
intercept_event.direction = -1

solution = solve_ivp(
    ode_function,
    t_span=(0.0, 20.0),
    y0=z0,
    args=(Vm, Vt, theta_t),
    events=intercept_event,
    max_step=0.01,
    rtol=1e-9,
    atol=1e-11
)


##### Lateral Acceleration Plot #####
_, a_lateral_g = dynamics(
    solution.t,
    solution.y,
    Vm,
    Vt,
    theta_t
)

plt.figure(figsize=(8, 5))

plt.plot(
    solution.t,
    a_lateral_g,
    color="purple",
    label="PN lateral acceleration"
)

plt.axhline(15, color="red", linestyle="--", label="+15 g limit")
plt.axhline(-15, color="red", linestyle="--", label="-15 g limit")

plt.xlabel("Time (s)")
plt.ylabel("Lateral acceleration (g)")
plt.title("Missile Lateral Acceleration")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


##### Trajectory Plot #####

xM = solution.y[0]
yM = solution.y[1]
xT = solution.y[2]
yT = solution.y[3]

plt.figure(figsize=(8, 5))

plt.plot(xM, yM, label="Missile")
plt.plot(xT, yT, label="Target")

plt.scatter(xM[0], yM[0], marker="o", label="Missile start")
plt.scatter(xT[0], yT[0], marker="s", label="Target start")
plt.scatter(xM[-1], yM[-1], marker="x", s=80, label="Intercept")

plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.title("PN Guidance Trajectory")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()

