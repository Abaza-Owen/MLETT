import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.cm as cm

filename = "sgdmldatasetnoec.npz"

dataset = np.load(filename , allow_pickle=True)
coordinates = dataset['R']


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

plt.figure(figsize=(10, 8))
plt.hist2d(x, y, bins=250, norm=LogNorm())
plt.colorbar(label='Intensity')
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Heatmap of XYZ Coordinate Pairs in {filename}')
plt.gca().invert_yaxis()  # Invert y-axis to match typical Cartesian coordinates
plt.show()

