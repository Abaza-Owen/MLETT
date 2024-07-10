import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import time 
# Load your dataset (replace with your actual dataset loading)
dataset = np.load("sgdmldatasetnoec.npz", allow_pickle=True)
coordinates = dataset['R']

# Extract x, y, z coordinates from your dataset
cx = []
cy = []
cz = []

for i in coordinates:
    for atom in i:
        cx.append(atom[0])
        cy.append(atom[1])
        cz.append(atom[2])

# Convert lists to numpy arrays for faster processing
#cx = np.array(cx)
#cy = np.array(cy)
#cz = np.array(cz)


x = []
y = []
z = []

x = cx
y = cy 
z = cz
print(len(x))
#x += cx[1::18]
#y += cy[1::18]
#z += cz[1::18]
#
#x += cx[2::18]
#y += cy[2::18]
#z += cz[2::18]
#
#
#x += cx[3::18]
#y += cy[3::18]
#z += cz[3::18]
#
#x += cx[1::18]
#y += cy[4::18]
#z += cz[4::18]
#
#x += cx[5::18]
#y += cy[5::18]
#z += cz[5::18]
#
ocur = np.random.rand(len(x))


# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot scatter plot with color mapping
img = ax.scatter(x, y, z, c=ocur, cmap=cm.Oranges_r, marker='o', s=2)

# Normalize scalar values for colormap
norm = plt.Normalize(ocur.min(), ocur.max())
sm = plt.cm.ScalarMappable(cmap=cm.Oranges_r, norm=norm)
sm.set_array([])  # Dummy mappable array needed for colormap normalization

# Add colorbar
#fig.colorbar(sm, ax=ax, label='Colorbar Title')

# Set labels and title
ax.set_title("3D Plot of Dataset Space Coverage for OH + CH2O -> HOH + CHO")
ax.set_xlabel('X-axis (Angstrom)')
ax.set_ylabel('Y-axis (Angstrom)')
ax.set_zlabel('Z-axis (Angstrom)')

ax.set_xlim([-10, 10])  # Example limits for X-axis
ax.set_ylim([-10, 10])  # Example limits for Y-axis
ax.set_zlim([-10, 10])
# Show the plot
plt.show()

