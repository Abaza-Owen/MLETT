import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import sys
from gausstrajlib import trajectory
from gausstrajlib import reader
from matplotlib.colors import LogNorm

#class DataFile():

#    def __init__(self, name, coordinates):
#        self.name = name 
#        self.coordinates = coordinates         


class DataPlot():
    
    def __init__(self):
        self.datasets = []       

    def heatmap(self, plane = 'xy', bins = 250):
        if len(self.datasets) > 1:
            print("[WARN]: More than one dataset loaded into memory with heatmap option specified. Heatmap only supports one loaded dataset. First dataset loaded will be used. (If using CLI, this is the first filename passed)")
        dataset = self.datasets[0]
        
        x = [comp[0] for comp in dataset.atom_xyz]
        y = [comp[1] for comp in dataset.atom_xyz]
        z = [comp[2] for comp in dataset.atom_xyz]
        
        I_AM_GOD =  {
            'x':x,
            'y':y,
            'z':z
        }
        
        planar_datasets = []        

        for c in plane: 
            try:
               planar_datasets.append(I_AM_GOD[c])     
            except Exception as e:
                print(f"plane {c} unrecognized")
        
        if (len(planar_datasets)) != 2:
            print('invalid number of planes passed')
            sys.exit()
        
        plt.figure(figsize=(10,8))
        plt.hist2d(planar_datasets[0], planar_datasets[1], bins = bins, norm = LogNorm())
        plt.colorbar(label = "Point Density")
        plt.xlabel(f"{plane[0]} - axis")
        plt.ylabel(f"{plane[1]} - axis")
        plt.title(f'Heatmap of XYZ Coordinate Pairs for {dataset.name}')
        plt.gca().invert_yaxis()
        plt.show()


    def scatterplot(self):
        colors = ('black','red', 'blue', 'green', 'yellow', 'purple')
        colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']    
        farthest_coord = 0
        title_base = "3D Scatter Plot of "

        names = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        for dataset, cm, cc in zip(self.datasets, colormaps, colors):
            x = [comp[0] for comp in dataset.atom_xyz]
            y = [comp[1] for comp in dataset.atom_xyz]
            z = [comp[2] for comp in dataset.atom_xyz]
    
            c = np.random.rand(len(x)) * 3 

            flattened_coords = [np.absolute(item) for sublist in dataset.atom_xyz for item in sublist]

            farthest_coord = max(flattened_coords) if max(flattened_coords) > farthest_coord else farthest_coord 
        
            a = max(c)            
            #ax.scatter(x, y, z, marker = 'o', s=5, c=c, cmap = cm)
            ax.plot(x, y, z, '.', markersize=5, color=cc, label=f'{dataset.name} Points')
            
            names.append(dataset.name)            

            #current_color = next(colors)

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




