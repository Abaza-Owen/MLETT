from gausstrajlib import trajectory as tj
import numpy as np
from gausstrajlib import conversions as cv
import traceback

class Reader():

    def __init__(self):
        pass
    
    def read_xyz(self, xyzname):
        coord_temp = []
        force_temp = []
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
                    coord_temp.append([x, y, z])
                    
                    fx = float(tokens[4])
                    fy = float(tokens[5])
                    fz = float(tokens[6])
                    
                    force_temp.append([fx, fy, fz])                
    
        print(f"Success reading from file {xyzname}")
        read_dataset = tj.Trajectory(name = xyzname, xyz = coord_temp, force = force_temp, units = cv.MSA)
        
        #s#elf.datasets.append(read_dataset)
        
        return [read_dataset]

    def read_npz(self, npzname):
        datasetnpz = np.load(npzname, allow_pickle=True)
        coordinates = datasetnpz['R']

        coord_temp = []    

        for i in coordinates:
            for atom in i:
                coord_temp[0].append(atom[0])
                coord_temp[1].append(atom[1])
                coord_temp[2].append(atom[2])
        
        read_dataset = tj.Trajectory(name = npzname, xyz = coord_temp, units = cv.SGDML)
        print(f"Success reading from file {npzname}")
        #self.datasets.append(read_dataset)   
        
        return [read_dataset]       
        

    def read_log(self, filename: str):
            # function internal to class to read a specific log file stored in the current working directory specified by name
            trajectories = []
            try:
                with open(filename, 'r') as log:
                    
                    sym_temp = [] #create empty temporary lists and important values
                    xyz_temp = []

                    forces_temp = []
                    vel_temp = []
                    eng_pot_temp = []
                    eng_kin_temp = []
                    
                    num_points = 128    
                    num_atoms = 0
                    multiplicity = 1
                    charge = 0

                    reint = 0 
                    e_trig = 0
                    last_line = ''
                    for line in log:
                        if ("Charge = " in line and "Multplicity = " in line ):

                            tokens = line.split
                            try:
                                multiplicity = int(tokens[2])
                            except ValueError as e:
                                print(e)
                                print("Could not convert multiplicity to numeric.")
                            try:
                                charge = int(tokens[5])
                            except ValueError as e:
                                print(e)
                                print("Could not convert multiplicity to numeric.")

                        if("Max. points for each Traj." in line): #get max cycles in a given trajectory. used to ensure that all points are written.

                            tokens = line.split()
                            num_points = int(tokens[6])

                        if ("Integration parameters:" in line): #handling of special case of first two gaussian trajectory steps.  

                            while("Input orientation" not in line):

                                line = next(log)
                            
                            while ("1" not in line.split()):

                                line = next(log)

                            num_atoms = 0

                            while (line[1] != '-'):

                                tokens = line.split()
                                sym = (tokens[1])
                                sym_temp.append(cv.ATOMIC_NUMBERS_TO_SYM[sym])
                                x = float(tokens[3]) / cv.ANG_PER_BOHR #convert first grabbed points from Angstrom to a.u for consistency 
                                y = float(tokens[4]) / cv.ANG_PER_BOHR
                                z = float(tokens[5]) / cv.ANG_PER_BOHR 
                                #xyz_temp.append([x, y, z])
                                num_atoms+=1
                                line = next(log)

                            while("***** Axes restored to original set *****" not in line ):

                                line = next(log)

                            while ("1" not in line.split()):

                               line = next(log)

                            while (line[1] != '-'):

                               tokens = line.split()
                               x = float(tokens[2])
                               y = float(tokens[3])
                               z = float(tokens[4])
                               force_hb = [x, y, z]
                               forces_temp.append(force_hb)
                               line = next(log)
            
                        if ("Reintegrating step number" in line):
                            reint += 1
                            print(len(xyz_temp))
                            xyz_temp = xyz_temp[:-6]
                            forces_temp = forces_temp[:-6]
                            vel_temp = vel_temp[:-6]
                            print('beep ', len(xyz_temp))
            
                        if ("Gradient from 2nd-fit:" in line):

                            line = next(log)

                            while (line.strip()):
                                tokens = line.split()
                                x = float(tokens[3].replace('D', 'E')) 
                                y = float(tokens[5].replace('D', 'E')) 
                                z = float(tokens[7].replace('D', 'E')) 
                                force_hb = [x, y, z]
                                forces_temp.append(force_hb)
                                line = next(log)
        
                        if ("Summary information for step" in line):

                            while ("Cartesian coordinates: (bohr)" not in line):
                                line = next(log)
                            line = next(log)
                            while ("MW" not in line.split()):
                                    #print(line)
                                    tokens = line.split()
                                    if ("MW" in line.split()):
                                        break
                                    x = float(tokens[3].replace('D', 'E')) 
                                    y = float(tokens[5].replace('D', 'E')) 
                                    z = float(tokens[7].replace('D', 'E')) 
                                    xyz_temp.append([x, y, z])
                                    line = next(log)

                            while ("MW cartesian velocity: (sqrt(amu)*bohr/sec)" not in line):
                                line = next(log)
                            line = next(log)
                            while(line.strip()):
                                tokens = line.split()
                                if("TRJ" in tokens[0] or 'I' not in tokens[0]):
                                    break
                                x = (tokens[3])
                                y = (tokens[5])
                                z = (tokens[7])
                                vel_temp.append([x,y,z])
                                line=next(log)

                        if ("Trajectory summary" == line.strip()): # Parse N Kinenetic and Potential Energies, where MaxSteps = N
                            while ("e" in line.strip()):
                                line = next(log)
                            while ("Max Error" not in line):
                                e_trig+=1
                                tokens = line.split()
                                e_kin_h = float(tokens[1])
                                e_pot_h = float(tokens[2])
                                eng_pot_temp.append(e_pot_h)
                                eng_kin_temp.append(e_kin_h)
                                line = next(log)
                            traj =  tj.Trajectory(name = filename, units = cv.AU, sym = sym_temp*num_points, xyz = xyz_temp, n_atoms = num_atoms, vel = vel_temp, force = forces_temp, ke = eng_kin_temp, pe = eng_pot_temp, mult = multiplicity, charge = charge)
                            trajectories.append(traj)
                            xyz_temp = xyz_temp[0:num_atoms]
                            print(len(xyz_temp))
                            print(len(xyz_temp))
                            forces_temp = forces_temp[0:num_atoms]
                            vel_temp = []
                            eng_pot_temp = []
                            eng_kin_temp = []
                        last_line = line

                print("Number of reintegrations", reint)
                #print("Number of coord triggers", coordtr)
                print("Energy Triggered?", e_trig)
                print("E")
                print(last_line)
                #traj =  tj.Trajectory(name = filename, units = cv.AU, sym = sym_temp*num_points, xyz = xyz_temp, n_atoms = num_atoms, vel = vel_temp, force = forces_temp, ke = eng_kin_temp, pe = eng_pot_temp, mult = multiplicity, charge = charge)
                #trajectories.append(traj)
                #trajectories.pop(0)


            
            except Exception as e:

                print(f"Error accessing file '{filename}': {e}")
                print(traceback.format_exception(e))
                return None
            else:
                print(f"Success reading from file {filename}")
                return trajectories


    def read_g_param(self, p_name):
        try:
            param_file = open(p_name, 'r')
            param = param_file.readlines()
            param_file.close()
            return param
        except Exception as e:
            print('Could not access the parameter file')
            print(e)


    def read(self, filename, format = 'intr'):
        
        read_formats = {
            'log':self.read_log,
            'xyz':self.read_xyz,
            'inp':self.read_xyz,
            'npz':self.read_npz 
        }
        file_ext = filename.split('.')[-1] if format == 'intr' else format            
        try:
            return read_formats[file_ext](filename)
        
        except KeyError as e:
            print('Specified file format not recognized. If implicit format declaration was used, try explicitly calling the format you would like.')
            print(e)
