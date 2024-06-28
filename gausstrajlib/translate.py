import os
#used for handling directory during read/write when needed
import sys
#used for terminating script in case of fatal error 
import traceback
#used for debugging. Debugging prints are commented out by default but can be reactivated in case of unexpected behavior
import math
#used for rounding down when indexing in write function.

#Per official documentation, Gaussian outputs in Angstroms for distances, Hartrees for energy, and Hartrees/Bohr for force 
#while sGDML assumes Angstroms, kcal/mol, and kcal/(mol*ang)
#MSA uses Hartrees/Bohr for gradient and Hartree for energies, but input geometry needs to be in Ang
#This section defines necessary constants for converting between the two values
ang_per_bohr=0.52917721092
#0.52917721092 Angstrom / Bohr Radius per CRC Handbook of Chemistry and Physics 93rd Edition
hart_per_kj= 4.35974434 * 10**-21
#4.35974434 * 10 ^ -21 Hartree / 1 kiloJoule per CRC Handbook of Chemistry and Physics 93rd Edition
avo =  6.02214129 * 10 ** 23
#6.02214129 obj / 1 mole per CRC Handbook of Chemistry and Physics 93rd Edition
kjmol_per_kcalmol = 4.184 
#4.184 kiloJoule/mole (thermochemical)/ 1 kilocalorie/mole per National Institute of Science and Technology (NIST) Physical Measurement Laboratory
kcalmol_per_hart = hart_per_kj * avo / kjmol_per_kcalmol
#approximately 627.5094742771939 kilocalorie/mole / 1 hartree 
kcalmolang_per_hartbohr = kcalmol_per_hart/ang_per_bohr
#approximately 1185.82105 kilocalorie/(mole*ang) / 1 hartree/bohr 


sgdml_conv = {
                'dist':ang_per_bohr, #Conversion to angstrom from bohr
                'eng':kcalmol_per_hart, #Conversion to kcal/mol from hartree
                'force':(-1 * kcalmolang_per_hartbohr) #Conversion to kcal/mol*ang from hartree/bohr * -1 to convert from gradient to force
                }
msa_conv = {
                'dist':ang_per_bohr, #Conversion to angstrom from bohr
                'eng':1,  #No conversion needed for MSA
                'force':1 #No conversion needed for MSA
                }

raw_conv = {
                'dist':1, #Conversion from bohr to bohr
                'eng':1, #Conversion from hartree to hartree
                'force':1 #Conversion from hartree/bohr to hartree/bohr
}

conversions = {
                'sgdml':sgdml_conv, #sGDML conversion dictionary
                'msa':msa_conv, #MSA conversion dictionary
                'raw':raw_conv  #Raw conversions (No change for debug or testing)             
                }


#dictionary for converting atomic numbers to symbols. Common symbols in our research used only. 
atomic_numbers_to_symbols = {
    '1': 'H',   # Hydrogen
    '6': 'C',   # Carbon
    '7': 'N',   # Nitrogen
    '8': 'O',   # Oxygen
    '15': 'P',  # Phosphorus
    '16': 'S',  # Sulfur
    '9': 'F',   # Fluorine
    '17': 'Cl', # Chlorine
    '35': 'Br', # Bromine 
    '80': 'Hg'  # Mercury
    
    # Add more elements as needed
}



class Trajectory():  #Trajectory object represents a completed Gaussian Trajectory. Basis for TrajData class. Defines lists (arrays) which hold information about atomic system. 

        def __init__(self, sym = [], xyz = [], force = [], n = 0, pe = [], ke = []): #__init__

                self._atomicity = n         #int    
                self._atom_symbols = sym    #list[str]
                self._atom_xyz = xyz        #list[list[float]]
                self._atom_forces = force   #list[list[float]] 
                self._sys_energy = pe       #list[float]
                self._sys_kin_energy = ke   #list[float]    
            

class TrajData(Trajectory): #Data-containing object meant to carry data from one .log Gaussian output files. Extension of Trajectory class. Includes important functions for manipulating and accessing data.

        def clear(self): #clears all values to default (empty lists of various types). Can be used to ensure previous data is deleted before a new read.
                    
                self._atomicity = 0         #int
                self._atom_symbols = []     #list[str]
                self._atom_xyz = []         #list[list[float]]
                self._atom_forces = []      #list[list[float]] 
                self._sys_energy = []       #list[float]
                self._sys_kin_energy = []   #list[float]

        def append_sym(self, syms: list[str]): #appends list of strings to 2d list of atomic symbols

                self._atom_symbols.append(syms)

        def append_xyz(self, xyzs: list[list[float]]): #appends 2dlist of floats to 3d list of atomic coordinates

                self._atom_xyz.append(xyzs)

        def append_forces(self, forces: list[list[float]]): #appends 2dlist of floats to 3d list of atomic forces

                self._atom_forces.append(forces)

        def append_energy(self, e):

                self._sys_energy.append(e)

        def append_kin_energy(self, e):

                self._sys_kin_energy.append(e)

        def set_sym(self, sym):

                self._atom_symbols = sym

        def set_xyz(self, xyz):

                self._atom_xyz = xyz

        def set_forces(self, forces):

                self._atom_forces = forces

        def set_atomicity(self, n):

                self._atomicity = n

        def set_energy(self, e):

                self._sys_energy = e

        def set_kin_energy(self, e):

                self._sys_kin_energy = e

        def get_atom_symbols(self): # returns 1dlist containing atomic symbols for each atom in every file read

                return self._atom_symbols

        def get_atom_xyz(self):     #returns 2dlist containing xyz coordinates for each atom in every file read

                return self._atom_xyz

        def get_atom_forces(self):  #returns 2dlist containing force vectors acting on each atom in every file read

                return self._atom_forces

        def get_atomicity(self):

                return self._atomicity

        def get_energy(self):

                return self._sys_energy

        def get_kin_energy(self):

                return self._sys_kin_energy

                              
class NullWriteError(Exception): #Custom error for used by the GaussianTranslator class which is thrown if data is somehow misread or an invalid (error termination) trajectory is used.

        def __init__(self, message = "Less data than expected to write to file. Check that file exists and run did not terminate in error."):
                    
                self.message = message
                super().__init__(self.message)
        
class GaussianTranslator(): #Object that facillitates the reading of .log files and writing to .xyz files in proper format. Main class of module.
        
        def __init__(self): #initializes empty instance of TrajData class, which holds relavant atomic symbols, xyz coords, forces, energies, etc.
                    
                self.trainData = TrajData()
  
        def __write_to_xyz__(self, outname: str, Data: TrajData(), grad = True, format = 'sgdml', eng_cnst = True, low_e = float('-inf'), high_e = float('inf')): #function internal to class for writing xyz format for sGDML
                
                try:
                    
                    #pull data into easier to access local lists
                    a_s = Data.get_atom_symbols()
                    a_xyz = Data.get_atom_xyz()
                    a_f = Data.get_atom_forces()
                    s_e = Data.get_energy()
                    
                    #define attributes important to indexing these lists in the writing steps to come
                    num_atoms = Data.get_atomicity()
                    num_xyz_sets = len(a_xyz)
                    num_energies = len(s_e)
                    num_steps = int(((len(a_s)/num_atoms)))
                    
                    #define conversion factors based off of format to be written 
                    eng_conv = conversions[format]['eng']
                    f_conv = conversions[format]['force']
                    d_conv = conversions[format]['dist']
                    
                    if num_atoms == 0:
                        raise NullWriteError()

                    if (num_energies != num_xyz_sets/num_atoms):
                        raise NullWriteError()
                    
                    with open(outname, 'w') as xyz:
                    
                        for j in range(num_xyz_sets):
                    
                            index = int(math.floor(j/num_atoms))
                    
                            if(s_e[index] > low_e and s_e[index] < high_e): #Energy cutoff for reactants in this range
                    
                                if(j%num_atoms == 0):
                    
                                    index = int(j/num_atoms)
                                    xyz.write(f"{num_atoms}\n") 
                    
                                    if(s_e):
                                        xyz.write(f"{s_e[index] * eng_conv}\n")
                                
                                current_xyz = a_xyz[j] #Format and convert xyz coordinates using dictionary conversions
                                current_xyz = [comp * d_conv for comp in current_xyz]
                                
                                current_forces = a_f[j] #Format and convert force/gradient values using dictionary conversions
                                current_forces = [comp * f_conv for comp in current_forces]
                    
                                symbol = a_s[j]
                    
                                coordinates = "\t".join(f"\t{coord:15.12f}" for coord in current_xyz)
                                forces = "\t".join(f"\t{force:15.12f}" for force in current_forces) if grad else ""
                                xyz.write(f"{symbol}\t{coordinates}\t{forces}\n")
                    
                    print(f"Success writing to file {outname}")

                except Exception as e:
                    print(f"An error occurred: {e}")
                   # traceback.print_exception(e)

        def __read_from_log_file__(self, filename: str):
                # function internal to class to read a specific log file stored in the current working directory specified by name

                self.trainData.clear()  # Resets data to prevent miswritting to instance of TrajData()

                try:
                    with open(filename, 'r') as log:
                        
                        sym_temp = [] #create empty temporary lists and important values
                        xyz_temp = []
                        forces_temp = []
                        eng_pot_temp = []
                        eng_kin_temp = []
                        num_points = 128    
                        num_atoms = 0

                        for line in log:
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
                                    sym_temp.append(atomic_numbers_to_symbols[sym])
                                    x = float(tokens[3]) / ang_per_bohr #convert first grabbed points from Angstron to a.u for consistency 
                                    y = float(tokens[4]) / ang_per_bohr
                                    z = float(tokens[5]) / ang_per_bohr 
                                    xyz_temp.append([x, y, z])
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

                                while("Cartesian coordinates: (bohr)" not in line):
                                    line = next(log)

                                line = next(log)

                                while ("MW" not in line.split()):
                                        tokens = line.split()
                                        if ("MW" in line.split()):
                                            break
                                        x = float(tokens[3].replace('D', 'E')) 
                                        y = float(tokens[5].replace('D', 'E')) 
                                        z = float(tokens[7].replace('D', 'E')) 
                                        xyz_temp.append([x, y, z])
                                        line = next(log)
                                        
                            if ("Reintegrating step number" in line):

                                xyz_temp = xyz_temp[:-6]
                                forces_temp = forces_temp[:-6]

                                while ("Gradient from 2nd-fit:" not in line):
                                    line = next(log)

                                line = next(log)

                                while (line.strip()):
                                    tokens = line.split()
                                    if ("TRJ" in tokens[0]):
                                        print("break")
                                        break
                                    x = float(tokens[3].replace('D', 'E')) 
                                    y = float(tokens[5].replace('D', 'E')) 
                                    z = float(tokens[7].replace('D', 'E'))
                                    force_hb = [x, y, z]
                                    forces_temp.append(force_hb)
                                    line = next(log)

                                while ("Cartesian coordinates: (bohr)" not in line):
                                    line = next(log)
                                line = next(log)

                                while ("MW" not in line.split()):
                                    tokens = line.split()
                                    if ("MW" in line.split()):
                                        break
                                    x = float(tokens[3].replace('D', 'E'))
                                    y = float(tokens[5].replace('D', 'E'))
                                    z = float(tokens[7].replace('D', 'E'))
                                    xyz_temp.append([x, y, z])
                                    line = next(log)
                            #parse all 500 energies and append to list

                            if ("Trajectory summary" == line.strip()):
                                while ("e" in line.strip()):
                                    line = next(log)
                                while ("Max Error" not in line):
                                    tokens = line.split()
                                    e_kin_h = float(tokens[1])
                                    e_pot_h = float(tokens[2])
                                    eng_pot_temp.append(e_pot_h)
                                    eng_kin_temp.append(e_kin_h)
                                    line = next(log)
                        
                        sym_temp = sym_temp * num_points
                        self.trainData.set_sym(sym_temp)
                        self.trainData.set_xyz(xyz_temp)
                        self.trainData.set_forces(forces_temp)
                        self.trainData.set_atomicity(num_atoms)
                        self.trainData.set_energy(eng_pot_temp)
                        self.trainData.set_kin_energy(eng_kin_temp)
                        
                        # Debugging prints
                        #print("Num forces:", len(self.trainData.get_atom_forces()))
                        #print("Num xyzs:", len(self.trainData.get_atom_xyz()))
                        #print("Num symbols:", len(self.trainData.get_atom_symbols()))
                        #print("Num energies:", len(self.trainData.get_energy()))

                    print(f"Success reading from file {filename}")

                except Exception as e:

                    print(f"Error accessing file '{filename}': {e}")

                   # traceback.print_exception(e)
            
        def get_read_data(self): #can be used to access data-containing object (for testing mostly)
                return self.trainData
            
        def read(self, path): #public function (accessible outside of class) which automatically calls the internal read function. Implemented in case an option to do read another file format is necessary to be implemented

                try:

                    self.__read_from_log_file__(path) 

                except Exception as e:

                    print(f"Error: read could not continue. Check arguments, including file and directory names are correct: \n {e}")
                   #sys.exit(1)
                
        def write(self, filename, test = False, grad = True, format = 'sgdml', eng_cnst = True, low_e = float('-inf'), high_e = float('inf')): #public function which calls internal __write_to_xyz_. Included for useability and to allow eventual expansion to other file types if necessary
                self.__write_to_xyz__(filename, self.trainData, grad = grad, format = format, eng_cnst = eng_cnst, low_e = low_e, high_e = high_e )
                #print(f"Failure in writing to file. Ensure test set is populated if attempting to write with test = True: {e} ")
        
