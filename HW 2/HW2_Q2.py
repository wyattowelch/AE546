import math
import numpy as np
import matplotlib.pyplot as plt

"""
Consider pursuit guidance, plot trajectories from Beta_0 -> 0
for a list of different gamma values. 

This is primarily a solve for part (a) in the question.
"""

gamma = np.array([2.0, 1.5, 1.0, 0.8])

Beta = np.flip(np.linspace(0.001, math.pi/2, 100)) # Beta_0 = pi/2

for g in gamma:
    R = ((np.tan(Beta/2)) ** g)/(np.sin(Beta))

    x = -R * np.cos(Beta)
    y = -R * np.sin(Beta)

    plt.plot(x, y, label=fr"$\gamma = {g}$")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Trajectories for Different Gamma Values \n Source: https://github.com/wyattowelch/AE546")
plt.axis("equal")
plt.grid()
plt.legend()
plt.show()
