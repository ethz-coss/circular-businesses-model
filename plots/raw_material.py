import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parameters import INITIAL_RAW_MATERIAL
import matplotlib.pyplot as plt
from my_environment.raw_material import RawMaterial

raw_material = RawMaterial()

# Generate data for the plot
amounts_taken = range(1, INITIAL_RAW_MATERIAL - 1000)  # Avoid complete depletion
costs = [raw_material.take_raw_material(1) for _ in amounts_taken]

# Plot the cost at each interval
plt.figure(figsize=(10, 6))
plt.plot(amounts_taken, costs, label="Cost of Raw Material", marker='o', linestyle='-')
plt.title("Cost of Raw Material Over Time")
plt.xlabel("Amount of Raw Material Taken")
plt.ylabel("Cost")
plt.grid(True)
plt.legend()
plt.show()