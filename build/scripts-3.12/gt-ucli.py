#!python

import sys
import os
import traceback
from gausstrajlib import translate as gt

class CommandLineHandler(): #small class which helps to clean and store command line arguments
    
    translator = gt.GaussianTranslator()

    def __init__(self):
        self.args = sys.argv
        self.num_args = len(self.args)  
        try:
            self.args = self._find_args_(self.args)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.print_usage_and_exit()

        self.input_path = self.args["input path"]   
        include_gradient = False
        format = 'sgdml'
        eng_cnst = True
        l_b = float('-inf')
        u_b = float('inf')
        if not self.args['input path'].endswith('.log'):
            self.print_usage_and_exit()
        if self.args['mode']:
            if 'g' in self.args['mode']:
                print('Gradients will be included in output file')
                include_gradient = True
            
            if 'm' in self.args['mode']:
                format = 'msa'
            
            if 'r' in self.args['mode']:
                format = 'raw'

            if 'ec' in self.args['mode']:
                try:
                    l_b = float(input("Input the minimum potential energy to be included in Hartree. (New line for no lower bound)"))
                except ValueError as e:
                    print("No valid value found. Set lower bound to negative infinity.")
                    l_b = float('-inf')
                try:
                    u_b = float(input("Input the maximum potential energy to be inlcuded in Hartree. (New line for no upper bound)"))
                except ValueError as e:
                    print("No valid value found. Set upper bound to infinity.")
                    u_b = float('inf')
                eng_cnst = False

            if 'd' in self.args['mode']:
                directory = os.listdir(os.getcwd())
                for filename in directory:
                    if filename.endswith('.log'):
                        file_out = filename.split(".")[0] + ".xyz"
                        self.translate(filename, file_out, grad = include_gradient, format = format, eng_cnst = eng_cnst, low_e = l_b, high_e = u_b)
            else:
                self.output_path = self.input_path.split(".")[0] + ".xyz" if not self.args['output path'] else self.args['output path']
                self.translate(self.input_path, self.output_path, grad = include_gradient, format = format, eng_cnst = eng_cnst, low_e = l_b, high_e = u_b)

    def translate(self, input_path, output_path, grad = False, format = 'sgdml', eng_cnst = True, low_e = float('-inf'), high_e = float('inf')):
        try:
                self.translator.read(input_path)
        except Exception as e:
                print(e)
                sys.exit()
        else:
                self.translator.write(output_path, grad = grad, format = format, eng_cnst = eng_cnst, low_e = low_e, high_e = high_e)

    
    def print_usage_and_exit(self):
        print("Incorrect number of arguments")
        print("Use: python gt-cli.py <mode> <path-in> or python gt-cli.py <path-in>")
        print("Recognized modes are -d and -f")
        print("Note that if reading a single file, the input must point to file ending in .log")
        print("See the readme file for more information")
        sys.exit(1)
        
    def _find_args_(self, args):
        mode = None
        input_path = None
        output_path = None
        for string in args:
            if string[0] == '-':
                mode = string 
            elif string.endswith('.log'):
                input_path = string
            elif '.' in string:
                output_path = string
        args = {
            'mode':mode,
            'input path':input_path,
            'output path':output_path
        }
        return args     
                    

        
cmd = CommandLineHandler()
