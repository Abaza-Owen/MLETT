import os
#used for handling directory during read/write when needed
import sys
#used for terminating script in case of fatal error 
import traceback
#used for debugging. Debugging prints are commented out by default but can be reactivated in case of unexpected behavior
import math
#used for rounding down when indexing in write function.
#from gausstrajlib import trajectory
from gausstrajlib import reader as rd
from gausstrajlib import writer as wr
#from gausstrajlib import errors
from gausstrajlib import conversions as cv


#dictionary for converting atomic numbers to symbols. Common symbols in our research used only. 


                              

        
class GaussianTranslator(): #Object that facillitates the reading of .log files and writing to .xyz files in proper format. Main class of module.
        
        conversions = {
                'sgdml':cv.SGDML_CONVERSIONS, #sGDML conversion dictionary
                'msa':cv.MSA_CONVERSIONS, #MSA conversion dictionary
                'raw':cv.RAW_CONVERSIONS  #Raw conversions (No change for debug or testing)             
                }
        
        def __init__(self): #initializes empty instance of TrajData class, which holds relavant atomic symbols, xyz coords, forces, energies, etc.
                pass
                

        def translate(self, input, output, grad = True, format = 'sgdml', low_e = float('-inf'), high_e = float('inf')):
                reader = rd.Reader()
                writer = wr.Writer()
                datafile = reader.read(input)
                for i in range(len(datafile.trajectories)):
                        datafile.trajectories[i].convert(self.conversions[format])
                        output = datafile.trajectories[i].name.split('.')[0] + str(i)  + '.xyz'
                        writer.write(output, datafile.trajectories[i], grad = grad, low_e = low_e, high_e = high_e) 


    
#        def read(self, path): #public function (accessible outside of class) which automatically calls the internal read function. Implemented in case an option to do read another file format is necessary to be implemented
#            formats = {#
#
#                'log':self.__read_from_log_file__
#
#           }
#
#           formats[path.split('.')[-1:]]()

                
#        def write(self, filename, grad = True, format = 'sgdml', low_e = float('-inf'), high_e = float('inf')): #public function which calls internal __write_to_xyz_. Included for useability and to allow eventual expansion to other file types if necessary
#                #print(f"Failure in writing to file. Ensure test set is populated if attempting to write with test = True: {e} ")
        
