import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import sys
from MLETT import trajectory
from MLETT import reader
from matplotlib.colors import LogNorm
from scipy.spatial import ConvexHull

#class DataFile():

#    def __init__(self, name, coordinates):
#        self.name = name 
#        self.coordinates = coordinates         


class DataPlot():
    
    def __init__(self):
        self.datasets = []       

    def heatmap(self, plane = 'xy', bins = 250, S = [3 , 5]):
       # if len(self.datasets) > 1:
       #     print("[WARN]: More than one dataset loaded into memory with heatmap option specified. Heatmap only supports one loaded dataset. First dataset loaded will be used. (If using CLI, this is the first filename passed)")
        xyz = [component for datafile in self.datasets for trajectory in datafile.trajectories for component in trajectory.atom_xyz]
        
        p_e = [component for datafile in self.datasets for trajectory in datafile.trajectories for component in trajectory.pot_energy]

        num_atoms = self.datasets[0].trajectories[0].atomicity 

        x = [comp[0] for comp in xyz]
        y = [comp[1] for comp in xyz]
        z = [comp[2] for comp in xyz]
        
        points_xyz = [[xyz[j] for j in range(num_atoms * i, (num_atoms)*(i+1))] for i in range(int(len(xyz)/num_atoms))]
        distances = [ np.linalg.norm(np.array(point[S[0]]) - np.array(point[S[1]])) for point in points_xyz]


 #       I_AM_GOD =  {
 #           'x':x,
 #           'y':y,
 #           'z':z
 #       }


        plt.figure(figsize=(10,8))
        plt.hist2d(distances, p_e, bins = bins, norm = LogNorm())
        plt.colorbar(label = "Densitity")
        plt.xlabel(f"Cartesian distance (Ang)")
        plt.ylabel(f"Potential Energy {self.datasets[0].trajectories[0].units['eng']}")
        plt.title(f'Heatmap of XYZ Coordinate Pairs for {self.datasets[0].name}')
        #plt.gca().invert_yaxis()
        plt.show()


    def scatterplot(self):
        colors = ('black','red', 'blue', 'green', 'yellow', 'purple')
        colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']    
        farthest_coord = 0
        title_base = "3D Scatter Plot of "

        names = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        for datafile, cm, cc in zip(self.datasets, colormaps, colors):
            xyz = [component for trajectory in datafile.trajectories for component in trajectory.atom_xyz]

            xyz = np.array(xyz)

            x = [comp[0] for comp in xyz]
            y = [comp[1] for comp in xyz]
            z = [comp[2] for comp in xyz]

            c = np.random.rand(len(x))  

            

            flattened_coords = [np.absolute(item) for sublist in xyz for item in sublist]

            farthest_coord = max(flattened_coords) if max(flattened_coords) > farthest_coord else farthest_coord 
        
            if len(self.datasets) == 1:    
                ax.scatter(x,y,z, marker = 'o', s=2, c=c, cmap = cm, label = f'{datafile.name} Points')
            else:
                ax.plot(x, y, z, '.', markersize=5, color=cc, label=f'{datafile.name} Points')
            
            names.append(datafile.name)            

        title_base += ', '.join(names)

        ax.set_title(title_base)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        
        ax.set_xlim([-farthest_coord, farthest_coord])
        ax.set_ylim([-farthest_coord, farthest_coord])
        ax.set_zlim([-farthest_coord, farthest_coord])

        ax.legend()

        plt.show()        

       
    def clear_datasets(self):
        self.datasets = []


#plotter.heatmap(plane = 'zy', bins = 5)




