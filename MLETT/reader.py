from MLETT import trajectory as tj
from MLETT import datafile as df
import numpy as np
from MLETT import conversions as cv
import traceback
import copy 


class Reader(): #Object to handling reading of several types of computational chemistry input files. 

    def __init__(self):
        pass
    
    def read_xyz(self, xyzname):
        datafile = df.DataFile(xyzname)
        coord_temp = []
        force_temp = []
        Z_temp = []
        p_e = []
        atomicity = 0

        with open(xyzname, 'r') as datasetxyz:
            lines = datasetxyz.readlines()
            try:
                atomicity = int(lines[0])
            except Exception as e:
                print("First line should be number of atoms in system as an integer. Please ensure proper formatting of xyz file and try again.")
                return            
            for i in range(len(lines)): # Skip the first two lines (header)
                
                if i %  (2 + atomicity) == 1:
                    p_e.append(float(lines[i])) 
                elif (i % (2+atomicity) != 0):
                    tokens = lines[i].split()
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
        read_dataset = tj.Trajectory(name = xyzname, 
                                     xyz = coord_temp, 
                                     force = force_temp,
                                     sym = Z_temp,
                                     n_atoms=atomicity,
                                     pe = p_e,
                                     units = cv.MSA)
        datafile.trajectories.append(read_dataset)
        return datafile

    def read_npz(self, npzname):
        datafile = df.DataFile(npzname)
        datasetnpz = np.load(npzname, allow_pickle=True)
        coordinates = datasetnpz['R']
        p_e = datasetnpz['E']
        forces = datasetnpz['F']
        coord_temp = [] 
        force_temp = []   
        
        atomicity = len(coordinates[0])
        print(atomicity)
        for pc,pf in zip(coordinates, forces):
            for ac, af in zip(pc,pf):
                coord_temp.append(ac)
                
                force_temp.append(af)
        
        read_dataset = tj.Trajectory(name = npzname, 
                                     xyz = coord_temp,
                                     n_atoms=atomicity,
                                     pe = p_e,
                                     force = force_temp, 
                                     units = cv.SGDML)
        
        print(f"Success reading from file {npzname}")
        
        datafile.trajectories.append(read_dataset)
        
        return datafile     
        

    def read_log(self, filename: str):
            # function internal to class to read a specific log file stored in the current working directory specified by name
            datafile = df.DataFile(name = filename) 
            # List to hold trajectories stored in file
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

                        if ("Charge = " in line and "Multplicity = " in line ): #Get system charge and Multiplicity. 

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

                        if("Max. points for each Traj." in line): #Get max cycles in a given trajectory. used to ensure that all points are written.

                            tokens = line.split()
                            num_points = int(tokens[6])

                        if ("Integration parameters:" in line): #Indiicates start of calculation in file. Handling of special case of first two gaussian trajectory steps .  

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
                               fx = float(tokens[2])
                               fy = float(tokens[3])
                               fz = float(tokens[4])
                               forces_temp.append([fx, fy, fz])
                               line = next(log)
            
                        if ("Reintegrating step number" in line): # Indicates last step did not meet criteria. 
                            reint += 1
                            # Delete last n entries in xyz, force, and velocity to allow for overwritting of bad step.
                            xyz_temp = xyz_temp[:-num_atoms]
                            forces_temp = forces_temp[:-num_atoms]
                            vel_temp = vel_temp[:-num_atoms]
            
                        if ("Gradient from 2nd-fit:" in line): # Indicates negative forces are to follow in units of Hartree/Bohr.  

                            line = next(log)
                            # Parse for all following gradient components
                            while (line.strip()):
                                tokens = line.split()
                                fx = float(tokens[3].replace('D', 'E')) 
                                fy = float(tokens[5].replace('D', 'E')) 
                                fz = float(tokens[7].replace('D', 'E'))  
                                forces_temp.append([fx, fy, fz])
                                line = next(log)
        
                        if ("Summary information for step" in line): # Indicates completion of step (whether it will be later reintegrated of not.). If statement added to prevent reading of predicited information.

                            while ("Cartesian coordinates: (bohr)" not in line):
                                line = next(log)
                            line = next(log)
                            while ("MW" not in line.split()):
                                    #print(line)
                                    tokens = line.split()
                                    if ("MW" in line.split()):
                                        break
                                    #Python does not recognize scientific notation using M * D+N. Replace D with E to allow for conversion to floating point number
                                    x = float(tokens[3].replace('D', 'E')) 
                                    y = float(tokens[5].replace('D', 'E')) 
                                    z = float(tokens[7].replace('D', 'E')) 
                                    # Add cartesian coordinates to xyz_temp
                                    xyz_temp.append([x, y, z])
                                    line = next(log)

                            while ("MW cartesian velocity: (sqrt(amu)*bohr/sec)" not in line): # Indiicates 
                                line = next(log)
                            line = next(log)
                            while(line.strip()):
                                # Parse velocity values
                                tokens = line.split()
                                if("TRJ" in tokens[0] or 'I' not in tokens[0]):
                                    break
                                vx = (tokens[3])
                                vy = (tokens[5])
                                vz = (tokens[7])
                                # Add xyz components of velocity to vel_temp
                                vel_temp.append([vx,vy,vz])
                                line=next(log)

                        if ("Trajectory summary" == line.strip()): # Indicates end of trajectory
                            # Parse N Kinenetic and Potential Energies where MaxSteps = N
                            while ("e" in line.strip()):
                                line = next(log)
                            while ("Max Error" not in line):
                                
                                e_trig+=1
                                # Parse and append kinetic and potential energy values at each step of Trajectory summary. 
                                tokens = line.split()
                                e_kin_h = float(tokens[1])
                                e_pot_h = float(tokens[2])
                                eng_pot_temp.append(e_pot_h)
                                eng_kin_temp.append(e_kin_h)
                                line = next(log)

                            #Create new trajectory object using data parsed
                            traj =  tj.Trajectory(name = filename, 
                                                  units = cv.AU, 
                                                  sym = sym_temp*num_points, 
                                                  xyz = xyz_temp, 
                                                  n_atoms = num_atoms, 
                                                  vel = vel_temp, 
                                                  force = forces_temp, 
                                                  ke = eng_kin_temp, 
                                                  pe = eng_pot_temp, 
                                                  mult = multiplicity, 
                                                  charge = charge)
                            #Add trajectory to list of tranjectories
                            datafile.trajectories.append(traj)
                            #Reset appropriate temporary values.
                            xyz_temp = []
                            forces_temp = forces_temp[0:num_atoms]
                            vel_temp = []
                            eng_pot_temp = []
                            eng_kin_temp = []

                print("Number of reintegrations", reint)
            
            except Exception as e:

                print(f"Error accessing file '{filename}': {e}")
                print(traceback.format_exception(e))
                #If Error occurs in reading, return nothing to prevent use of bad data.
                return None 
            else:
                print(f"Success reading from file {filename}")
                #Return list of all trajectories contained in .log file. 
                return datafile 

    def read_g_param(self, p_name): # Read all lines of parameter file used to specify options and title block for gaussian input files when extending a log file. 
        try:
            param_file = open(p_name, 'r')
            param = param_file.readlines()
            param_file.close()
            return param
        except Exception as e:
            print('Could not access the parameter file')
            print(e)


    def read(self, filename, format = 'imp'):
        
        # Dictionary of various read functions keyed by their associated file extension
        read_formats = {
            'log':self.read_log,
            'xyz':self.read_xyz,
            'inp':self.read_xyz,
            'npz':self.read_npz 
        }

        # If implicit format declaration is used (format == 'imp', default), the file extension is used to call the appropriate function. 
        # Otherwise, format can be explicitly declared by passing format = 'extension' for the format of your choice. 
        file_ext = filename.split('.')[-1] if format == 'imp' else format 

        # Try to call correct function. Error if an invalid extension is used. 
        try:
            return read_formats[file_ext](filename)
        
        except KeyError as e:
            print('Specified file format not recognized. If implicit format declaration was used, try explicitly calling the format you would like.')
            print(e)
