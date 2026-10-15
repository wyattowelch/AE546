"""
2-D Iterative Guidance Mode (IGM) learning scaffold.

This file intentionally does NOT solve the IGM math for you.  It provides:

    1. Editable inputs with units and expected sizes.
    2. General step labels matching the Ascent Guidance slides.
    3. Empty function shells where you can translate each slide into Python.
    4. Shape/residual checks and plots to verify your completed work.

Reference slides:
    Ascent Guidance-short.pdf, especially slides 35-44.

Suggested dependencies:
    python3 -m pip install numpy matplotlib scipy

SciPy is not required for the setup below.  It is included as an optional
tool later if you want to numerically integrate your completed dynamics.
"""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


"""
INPUTS AND OUTPUTS TO REFER TO WHEN MODIFYING THIS FILE
=======================================================

Current vehicle state at t0:
    t0                  scalar [s]
    x0, y0              scalars [m]
    vx0, vy0            scalars [m/s]
    m0                  scalar [kg]

Vehicle/engine values:
    T                   scalar, constant thrust [N]
    Isp                 scalar, specific impulse [s]
    g0                  scalar, standard gravity [m/s^2]
    g                   scalar, constant downward gravity magnitude [m/s^2]

Terminal targets:
    target_y            scalar, final altitude [m]
    target_vx           scalar, final horizontal velocity [m/s]
    target_vy           scalar, final vertical velocity [m/s]
    target_x            None here because x(tf) is free in the slide example

Unknowns that you will eventually calculate:
    mdot                scalar [kg/s]
    tgo                 scalar [s]
    chi_tilde           scalar [rad]
    k1                  scalar [1/s]
    k2                  scalar [rad]
    beta_command        scalar [rad]

Time-history arrays that your completed code should produce:
    time                shape (N,) [s]
    x, y                shape (N,) [m]
    vx, vy              shape (N,) [m/s]
    mass                shape (N,) [kg]
    beta               shape (N,) [rad]

The code currently initializes these outputs as None/NaN.  Replace them only
after working through the matching slide and writing that part yourself.
"""


# ============================================================================
# EDITABLE INPUTS
# ============================================================================

t0 = 0.0
x0, y0 = 0.0, 0.0
vx0, vy0 = 0.0, 0.0
m0 = 10_000.0

T = 500_000.0         # [N]
Isp = 300.0            # [s]
g0 = 9.80665           # [m/s^2]
g = 9.80665            # [m/s^2]

target_x = None        # Intentionally free in this 2-D example.
target_y = 23_400.0    # [m]
target_vx = 364.2826    # [m/s]
target_vy = 1771.7499   # [m/s]

# Temporary plotting time grid.  Replace tf_guess after you estimate t_go.
tf_guess = 30.0        # [s]
N = 500                # number of plotting/integration points
time = np.linspace(t0, tf_guess, N)

# Set True only after you have populated the result arrays below.
RUN_PLOTS = False


# ============================================================================
# RESULT VARIABLES TO FILL IN WHILE WORKING THROUGH THE SLIDES
# ============================================================================

# Scalar results.  Leave as None until you calculate them.
mdot = None
tgo = None
tf = None
chi_tilde = None
k1 = None
k2 = None
beta_command = None

# Time-history results.  Replace np.nan arrays with your calculated histories.
x = np.full_like(time, np.nan)
y = np.full_like(time, np.nan)
vx = np.full_like(time, np.nan)
vy = np.full_like(time, np.nan)
mass = np.full_like(time, np.nan)
beta = np.full_like(time, np.nan)


# ============================================================================
# STEP-BY-STEP LEARNING WORKFLOW
# ============================================================================

def step_1_initialize_problem():
    """Step 1: define the current state, engine model, and terminal targets."""

    # Check that the input values have sensible signs and units.
    # Keep this step simple: no guidance math belongs here.
    if m0 <= 0.0:
        raise ValueError("m0 must be positive.")
    if T <= 0.0 or Isp <= 0.0 or g0 <= 0.0 or g <= 0.0:
        raise ValueError("T, Isp, g0, and g must be positive.")


def step_2_remove_final_position_constraints_first():
    """Step 2: temporarily remove final-position constraints.

    This is the main idea from slides 36-37.  First solve the velocity-only
    problem so the thrust angle is constant and the equations are integrable.
    In this example, both x(tf) and y(tf) are ignored during this pass.
    """

    # TODO: Starting from slides 36-37, write the constant-angle solution.
    # You should determine the angle chi_tilde from the velocity targets.
    # Use atan2 rather than atan when you are ready to preserve the quadrant.
    raise NotImplementedError("Work through slides 36-37 and implement this step.")


def step_3_estimate_time_to_go():
    """Step 3: estimate t_go using the required velocity increment."""

    # TODO: Follow slides 38-39.
    # 1. Make an initial guess for t_go.
    # 2. Calculate the velocity-to-be-gained using the previous t_go guess.
    # 3. Use the one-dimensional rocket equation to update t_go.
    # 4. Repeat until the change in t_go is below your tolerance.
    raise NotImplementedError("Work through slides 38-39 and implement this step.")


def step_4_restore_altitude_constraint():
    """Step 4: restore y(tf)=y* with the linear-tangent approximation."""

    # TODO: Follow slides 41-42.
    # Write the approximate thrust angle and the first-order sine/cosine
    # expressions as shown in the slides.  Keep the approximation visible in
    # your code instead of hiding it inside a helper function.
    raise NotImplementedError("Work through slides 41-42 and implement this step.")


def step_5_solve_for_k1_and_k2():
    """Step 5: form and solve the two equations for k1 and k2."""

    # TODO: Follow slides 43-44.
    # 1. Integrate the approximate equations to obtain y(tf) and Vy(tf).
    # 2. Set y(tf)=y*.
    # 3. Equate the corrected Vy equation to the velocity-only Vy equation.
    # 4. Write the two equations as a 2x2 linear system.
    # 5. Solve that system with np.linalg.solve after you understand each term.
    raise NotImplementedError("Work through slides 43-44 and implement this step.")


def step_6_form_current_thrust_command():
    """Step 6: calculate the current thrust-angle command."""

    # TODO: Use the final relationship on slide 44.
    # The guidance command is evaluated at the current time t0.
    raise NotImplementedError("Use slide 44 to implement the current command.")


def dynamics_for_optional_numerical_check(t, state):
    """Optional ODE shell for checking your closed-form solution.

    State order should be [x, y, vx, vy, mass].  This function is intentionally
    incomplete so you must translate the equations of motion from slide 35.
    Once written, it can be passed to scipy.integrate.solve_ivp.
    """

    # TODO: Implement the five state derivatives from slide 35.
    # Remember that the thrust direction comes from your beta command.
    raise NotImplementedError("Translate the slide 35 equations here.")


def step_7_check_shapes_and_residuals():
    """Step 7: check the outputs before looking at the plots."""

    histories = {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "mass": mass,
        "beta": beta,
    }

    for name, values in histories.items():
        values = np.asarray(values)
        if values.shape != time.shape:
            raise ValueError(f"{name} must have shape {time.shape}, not {values.shape}.")

    if not all(np.all(np.isfinite(values)) for values in histories.values()):
        print("\nOutput histories still contain NaN/inf values.")
        print("Complete the TODO steps before running the verification plots.")
        return

    print("\nTerminal residuals from your filled-in arrays:")
    print(f"  altitude residual y(tf)-y*   = {y[-1] - target_y:.6e} m")
    print(f"  Vx residual Vx(tf)-Vx*       = {vx[-1] - target_vx:.6e} m/s")
    print(f"  Vy residual Vy(tf)-Vy*       = {vy[-1] - target_vy:.6e} m/s")


def plot_verification_results():
    """Plot the histories you calculate; this function does no guidance math."""

    step_7_check_shapes_and_residuals()

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(x, y, label="Your calculated trajectory")
    ax.axhline(target_y, color="k", ls="--", label="Target altitude y*")
    ax.set_title("Trajectory")
    ax.set_xlabel("Downrange x [m]")
    ax.set_ylabel("Altitude y [m]")
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(time, vx, label="Vx")
    ax.plot(time, vy, label="Vy")
    ax.axhline(target_vx, color="C0", ls="--", label="Vx*")
    ax.axhline(target_vy, color="C1", ls="--", label="Vy*")
    ax.set_title("Velocity")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Velocity [m/s]")
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax = axes[1, 0]
    ax.plot(time, np.degrees(beta), label="Your beta(t)")
    if beta_command is not None:
        ax.scatter([t0], [math.degrees(beta_command)], color="red", label="beta(t0)")
    ax.set_title("Thrust angle")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Angle [deg]")
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax = axes[1, 1]
    ax.plot(time, mass, label="Your m(t)")
    ax.set_title("Mass")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Mass [kg]")
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.show()


def main():
    """Run only setup/checks by default; enable plots after filling the TODOs."""

    step_1_initialize_problem()

    print("IGM learning scaffold loaded.")
    print("The solver steps are intentionally incomplete.")
    print("Work through the TODO functions in slide order: 36-37, 38-39, 41-44.")

    if RUN_PLOTS:
        plot_verification_results()


if __name__ == "__main__":
    main()

