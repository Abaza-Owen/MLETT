import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib

#matplotlib.interactive(True)

matplotlib.use('Qt5Agg')  

# Load your dataset (replace with your actual dataset loading)
dataset = np.load("combineddata.npz", allow_pickle=True)
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

x = np.array(x)
y = np.array(y)
z = np.array(z)


print(len(x))
print(len(y))
print(len(z))


# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Generate a scalar value (replace with your actual data or calculation)
ocur = np.random.rand(len(x))

# Plot scatter plot with color mapping
img = ax.scatter(x, y, z, c=ocur, cmap=cm.Oranges_r, marker='+', s=15)

# Normalize scalar values for colormap
norm = plt.Normalize(ocur.min(), ocur.max())
sm = plt.cm.ScalarMappable(cmap=cm.Oranges_r, norm=norm)
sm.set_array([])  # Dummy mappable array needed for colormap normalization

# Add colorbar
fig.colorbar(sm, ax=ax, label='Colorbar Title')

# Set labels and title
ax.set_title("3D Heatmap")
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
fig.show()
plt.show()

