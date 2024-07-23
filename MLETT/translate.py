import os
#used for handling directory during read/write when needed
import sys
#used for terminating script in case of fatal error 
import traceback
#used for debugging. Debugging prints are commented out by default but can be reactivated in case of unexpected behavior
import math
#used for rounding down when indexing in write function.
#from GTT import trajectory
from GTT import reader as rd
from GTT import writer as wr
#from GTT import errors
from GTT import conversions as cv


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
                print(output)
                try:
                        for i in range(len(datafile.trajectories)):
                                datafile.trajectories[i].convert(self.conversions[format])
                                outtraj = output.split('.')[-2] + '_T' + str(i+1)  + '.xyz'
                                writer.write(outtraj, datafile.trajectories[i], grad = grad, low_e = low_e, high_e = high_e) 
                except Exception as e:
                        print(e)
                        print(f"No or incomplete data found in {input}. Could not write.")
                
