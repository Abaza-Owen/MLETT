import os
#used for handling directory during read/write when needed
import sys
#used for terminating script in case of fatal error 
import traceback
#used for debugging. Debugging prints are commented out by default but can be reactivated in case of unexpected behavior
import math
#used for rounding down when indexing in write function.
from gausstrajlib import conversions as cv

class Trajectory():  #Trajectory object represents a completed Gaussian Trajectory. Basis for TrajData class. Defines lists (arrays) which hold information about atomic system. 

        def __init__(self, name = '', sym = [], vel = [[],[],[]], xyz = [[],[],[]], force = [], n_atoms = 0, pe = [], ke = [], units = cv.AU, mult = 1, charge = 0, bonding = '0'): #__init__
                self.name = name           #str
                self.atomicity = n_atoms   #int    
                self.atom_symbols = sym    #list[str]
                self.atom_xyz = xyz        #list[list[float]]
                self.atom_forces = force   #list[list[float]] 
                self.atom_vel = vel        #list[list[float]]
                self.pot_energy = pe       #list[float]
                self.kin_energy = ke       #list[float]
                self.units = units         #dictionary[str:str] 
                self.mult = mult
                self.charge = charge
                self.bonding = bonding


        def clear(self): #clears all values to default (empty lists of various types). Can be used to ensure previous data is deleted before a new read.
                
                self.name = ''             #str    
                self.atomicity = 0         #int
                self.atom_symbols = []     #list[str]
                self.atom_xyz = [[],[],[]]         #list[list[float]]
                self.atom_forces = [[],[],[]]      #list[list[float]] 
                self.atom_vel = [[],[],[]]         #list[list[float]]
                self.pot_energy = []       #list[float]
                self.kin_energy = []   #list[float]

        def convert(self, conversions):
            #dictionary of conversion factors for values desired to converted. Missing keys in dictionary will signify no conversion.
            try:
                distance_conv = conversions['dist']
                for i in range(len(self.atom_xyz)):
                    for j in range(len(self.atom_xyz[i])):
                        self.atom_xyz[i][j] *=  distance_conv
            except KeyError as e:
                pass
            
            try:
                force_conv = conversions['force']
                for i in range(len(self.atom_forces)):
                    for j in range(len(self.atom_forces[i])):
                        self.atom_forces[i][j] *= force_conv
            except KeyError as e:
                pass
            try:
                eng_conv = conversions['eng']
                for i in range (len(self.pot_energy)):
                    self.pot_energy[i] *= eng_conv
                    self.kin_energy[i] *= eng_conv 
            except KeyError as e:
                pass
            try:
                vel_conv = conversions['vel']
                for i in self.atom_vel:
                    self.atom_vel[i] *= vel_conv
            except KeyError as e:
                pass

            try:
                self.units = conversions['units']
            except KeyError as e:
              self.units = self.units