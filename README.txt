Using the Machine Learning Energy Translation and Trimming and gt-cli Script
6/4/2024
Owen M. Abaza
SUNY ESF
omabaza@syr.edu
____________________________________________________________________________________________________________________________________________________________________________
Explanation:

The Machine Learning Energy Translation and Trimming and it's command line interface, 
Gaussian Translation - Unified Command Line Interface (gt-ucli), 
are designed to extract the forces, potential energies, and coordinates of all atoms in system
at every step of a Gaussian BOMD trajectory simulation. These extracted values can be 
converted from atomic units (a.u) to Ang and kcal/mol, which is the standard
for sGDML or kept in original format depending on the command line options chosen. 
This is output as an extended xyz file (.xyz). 

If using sgdml, this .xyz file can then be read directly from a python script using the sGDML.io.readxyz() function
or can be converted to a numpy array file (.npz) using the script sgdml_dataset_fromextxyz.py <filename>

MSA will read the .xyz file directly by default.

MLETT has additional functionalities including plotting a dataset, or group of datasets in 3D space, plotting bond distances vs energy as a heatmap, 
trimming dataset by interatomic distances, grouping like atoms together in a dataset file to help take advantage of symmetry, and creating .gjf files from a .log file.

Most of these functionalities were tasks that I found useful or necessary in the process of developing models from our test system and so they were included here. 
If you meet a challenge that requires a different functionality feel free to reach out to me and I will do my best to accomodate.  
____________________________________________________________________________________________________________________________________________________________________________
Requirements: 

	Python Version >= 3.6
	  Numpy >= 2.0
	  Matplotlib >= 3.4.3

	A properly configured Python virtual environment

	As of now, a LINUX environment

____________________________________________________________________________________________________________________________________________________________________________
Installation:

In order to download this library, download the .tar file and place it in appropriate location in your home directory on the UNIX machine. 
Use tar -xf GTT-1-0-0.tar to extract the archive and navigate into the extracted folder. Then with the virtual environment active for which 
you wish to install these the library and scripts, type

	pip install .

Pip will print some text to the console with information about the operations be completed. Pip will be clear if there is an error in the process. If there is,
it may mean that I configured something incorrectly, so feel free to contact me. 

Alternatively, you can use the git command to download the repository directly from github to your home directory and use pip as shown above to install.
If you have questions about this navigate to github and click on the down arrow near Code on the webpage and it will show you how to achive this.

Once you have installed the library using pip and have verified that it works as intended, you can delete the GTT folder.
____________________________________________________________________________________________________________________________________________________________________________
Usage:

In order to run these scripts, simply open a UNIX terminal window
and run the following command:

	gt-ucli <mode> <options> <file-input> <file-output>
	
The ouput file name is optional, and is only supported for certain modes/options. 
if it is not included the output file will simply have the same name as the input file with the .xyz extension.


Once it has run, your file should appear in the same directory as you have specified. 
You can then open this with a text editor and verify that each step corresponds 
correctly between the xyz file and log file. Note that the step numbers in the
.log file will be one greater than the corresponding step in Gaussview and the 
xyz file as Gaussian16 does an initilization step that gathers the inital 
geometry and velocities with no calculation of gradient or potential energy. 

mode:
  "convert":
    options:		
      input method:
        -f		          (file) Parse and Write from one specified .log file (default)
        -d 	  	        (directory) Parse and Write from all .log files in current working directory
    output content:
        -g	    	      (gradient) Include gradient/force in output XYZ, necessary for sGDML, optional for MSA
    output format:
        -s              (sGDML) SGDML file format (Force: kcal/mol*ang, Dist: Ang, Eng: kcal/mol) (default)
        -m		          (MSA) MSA file format (Force: Hartree/Bohr, Dist: Ang, Eng: Hartree)
        -r  	  	      (Raw) Raw file format. For testing only. (Force: Hartree/Bohr, Dist: Bohr, Eng: Hartree) 
    
    "trim":
      options:
        --S a1 a2         (vector) Establishes interatomic vector representing which pairing should be used to assess a maximum distance
        --d max_dist      (float distance) Specifies the maximum distance between the atoms specified in the 'S' vector a given datapoint can have without being trimmed
        --lb min_energy   (float energy) Specifies minimum energy, in whatever unit the dataset original had, that a datapoint can have without being trimmed
        --hb max_energy   (float energy) Specifies minimum energy, in whatever unit the dataset original had, that a datapoint can have without being trimmed
    
    "heatmap":
      options:
        --S a1 a2         (vector) Establishes interatomic vector representing which pairing should be used to assess interatomic distance for plotting
        --bins integer    (integer) Specifies the number of bins for the heatmap. A higher number corresponds to finer detail, but smaller datasets tend to suffer in visibility.
    
    "group":
      n/a as of the latest release
    
    "scatter":
      n/a as of the latest release

Input filenames and output filenames will be ignored if the -d option is used with the convert functionality. 
All .log files in the directory will be parsed and their output will be written to a file corresponding to the parent filename
with the .xyz extension substituted for .log.

It is important to note that this script was written with BOMD AM1 and wB97XD trajectories
in mind. If you are finding that it does not work as expected for a Gaussian job
using a different method or level of theory you can try to modify the script.
Otherwise, please email me a copy of the script that you are using along with the output file
it is not working correctly with, and I will try to modify the script to work for your job as
soon as possible.
____________________________________________________________________________________________________________________________________________________________________________
Questions:
Always feel free to shoot me an email at the address above. I will do my best to help you.

