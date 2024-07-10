import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import sys
from matplotlib.colors import LogNorm

class DataFile():

    def __init__(self, name, coordinates):
        self.name = name 
        self.coordinates = coordinates         


class DataPlot():
    
    def __init__(self):
        self.datasets = []       

    def read_xyz(self, xyzname):
        coord_temp = [[], [], []]
        Z_temp = []
        atomicity = 0
        with open(xyzname, 'r') as datasetxyz:
            lines = datasetxyz.readlines()
            for line in lines: # Skip the first two lines (header)
                if len(line.split()[0]) <= 2 and len(line.split()) > 1:
                    tokens = line.split()
                    Z_temp.append(tokens[0])
                    x = float(tokens[1])
                    y = float(tokens[2])
                    z = float(tokens[3])
                    coord_temp[0].append(x)
                    coord_temp[1].append(y)
                    coord_temp[2].append(z)
        
        read_dataset = DataFile(xyzname, coord_temp)
        
        self.datasets.append(read_dataset)
        
        return coord_temp

    def read_npz(self, npzname):

        datasetnpz = np.load(npzname, allow_pickle=True)
        coordinates = datasetnpz['R']

        coord_temp = [[],[],[]]    

        for i in coordinates:
            for atom in i:
                coord_temp[0].append(atom[0])
                coord_temp[1].append(atom[1])
                coord_temp[2].append(atom[2])
        
        read_dataset = DataFile(npzname, coord_temp)
        
        self.datasets.append(read_dataset)   
        
        return coord_temp       

    def heatmap(self, plane = 'xy', bins = 250):
        if len(self.datasets) > 1:
            print("[WARN]: More than one dataset loaded into memory with heatmap option specified. Heatmap only supports one loaded dataset. First dataset loaded will be used. (If using CLI, this is the first filename passed)")
        dataset = self.datasets[0]
        x = dataset.coordinates[0]
        y = dataset.coordinates[1]
        z = dataset.coordinates[2]

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


    def scatterplot(self ):
        colors = ('black','red', 'blue', 'green', 'yellow', 'purple')
        colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']    
        farthest_coord = 0
        marker_size = [1 , 500 , 1500]
        title_base = "3D Scatter Plot of "

        names = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        orda = [1 , 5, 10]
        for dataset, cc, s, cm, p in zip(self.datasets, colors, marker_size, colormaps, orda):
            x, y, z = dataset.coordinates
    
            c = np.random.rand(len(x)) * 3 

            flattened_coords = [np.absolute(item) for sublist in dataset.coordinates for item in sublist]

            farthest_coord = max(flattened_coords) if max(flattened_coords) > farthest_coord else farthest_coord 
            
            print(dataset.name)
            print(cm)
            print(s)
            a = max(c)            
            ax.scatter(x, y, z, marker = 'o', s=s, c=c, cmap = cm, zorder = p)
            #ax.plot(x, y, z, '.', markersize=s, color=cc, label=f'{dataset.name} Points')
            
            names.append(dataset.name)            

            #current_color = next(colors)

        title_base += ', '.join(names)

        ax.set_title(title_base)
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')
        
        print(farthest_coord)

        ax.set_xlim([-farthest_coord, farthest_coord])
        ax.set_ylim([-farthest_coord, farthest_coord])
        ax.set_zlim([-farthest_coord, farthest_coord])

        ax.legend()

        plt.show()        

       
    def clear_datadsets(self):
        self.datasets = []


plotter = DataPlot()

plotter.read_npz("sgdmldatasetnoec.npz")
plotter.read_xyz("comt.xyz")
plotter.read_xyz("sgdmldatasetnoecpt19996.xyz")
plotter.scatterplot()

#plotter.heatmap(plane = 'zy', bins = 5)




