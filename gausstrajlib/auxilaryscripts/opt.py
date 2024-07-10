import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib

#matplotlib.interactive(True)

matplotlib.use('Qt5Agg')  

# Load your dataset (replace with your actual dataset loading)
dataset = np.load("subset_9000pts.npz", allow_pickle=True)
coordinates = dataset['R']

# Extract x, y, z coordinates from your dataset (modify as per your data structure)
x = []
y = []
z = []

for i in coordinates:
    for atom in i:
        x.append(atom[0])  # Assuming atom[0] is x coordinate
        y.append(atom[1])  # Assuming atom[1] is y coordinate
        z.append(atom[2])  # Assuming atom[2] is z coordinate

# Enable interactive mode
#plt.ion()
# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generate a scalar value (replace with your actual data or calculation)

# Plot scatter plot with color mapping
img = ax.scatter(x, y, z, cmap = 'viridis')

# Normalize scalar values for colormap
fig.colorbar(img)

# Set labels and title
ax.set_title("3D Heatmap")
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

ax.set_xlim([-10, 10])  # Example limits for X-axis
ax.set_ylim([-10, 10])  # Example limits for Y-axis
ax.set_zlim([-10, 10])
fig.show()
plt.show()

