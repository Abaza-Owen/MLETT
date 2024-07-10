import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_xyz(xyzname):
    coord_temp = [[], [], []]
    Z_temp = []
    atomicity = 0
    with open(xyzname, 'r') as xyz:
        lines = xyz.readlines()
        for line in lines: # Skip the first two lines (header)
            if len(line.split()) > 1:
                tokens = line.split()
                Z_temp.append(tokens[0])
                x = float(tokens[1])
                y = float(tokens[2])
                z = float(tokens[3])
                coord_temp[0].append(x)
                coord_temp[1].append(y)
                coord_temp[2].append(z)
    return coord_temp

# Input file names
datafilename = input("Dataset file: ")
testfilename = input("Test file: ")

# Read data from files
dataset = read_xyz(datafilename)
testset = read_xyz(testfilename)

# Extract x, y, z coordinates from dataset and testset
dx, dy, dz = dataset
tx, ty, tz = testset

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot dataset points in grey
ax.plot(dx, dy, dz, '.', markersize=2, color='grey', label='Dataset Points')

# Plot testset points in red
ax.plot(tx, ty, tz, '.',  markersize=2, color='red', label='Testset Points')

# Set labels and title
ax.set_title("3D Scatter Plot")
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.set_xlim([-10, 10])  # Example limits for X-axis
ax.set_ylim([-10, 10])  # Example limits for Y-axis
ax.set_zlim([-10, 10])
# Add a legend
ax.legend()

# Show the plot
plt.show()

