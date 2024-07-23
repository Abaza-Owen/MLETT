Using the Gaussian Trajectory Translation and gt-cli Script
6/4/2024
Owen M. Abaza
SUNY ESF
omabaza@syr.edu
____________________________________________________________________________________________________________________________________________________________________________
Explanation:

The Gaussian Trajectory Translation library and it's command line interface, 
Gaussian Trajectory Translation - Unified Command Line Interface (gtt-ucli), 
are designed to extract the forces, potential energies, and coordinates of all atoms in system
at every step of a Gaussian BOMD trajectory simulation. These extracted values can be 
converted from atomic units (a.u) to Ang and kcal/mol, which is the standard
for sGDML or kept in original format depending on the command line options chosen. 
This is output as an extended xyz file (.xyz). 

If using sgdml, this .xyz file can then be read directly from a python script using the sGDML.io.readxyz() function
or can be converted to a numpy array file (.npz) using the script sgdml_dataset_fromextxyz.py <filename>

MSA will read the .xyz file directly by default.

GTT has additional functionalities including plotting a dataset, or group of datasets in 3D space, plotting bond distances vs energy as a heatmap, 
trimming dataset by interatomic distances, grouping like atoms together in a dataset file to help take advantage of symmetry, and creating .gjf files from a .log file.

Most of these functionalities were tasks that I found useful or necessary in the process of developing models from our test system and so they were included here. 
If you meet a challenge that requires a different functionality feel free to reach out to me and I will do my best to accomodate.  
____________________________________________________________________________________________________________________________________________________________________________
Requirements: 

	Python Version >= 3.6
	  Numpy
	  Scipy 
	  Matplotlib

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

option		function
input method:
-f		(file) Parse and Write from one specified .log file (default)
-d 		(directory) Parse and Write from all .log files in current working directory
output content:
-g		(gradient) Include gradient/force in output XYZ, necessary for sGDML, optional for MSA
-ec		(energy constraints) Filter out points wiht potential energies above a certain threshold. You will be prompted for higher and lower constraints once the program runs. 
output format:
-s 		(sGDML) SGDML file format (Force: kcal/mol*ang, Dist: Ang, Eng: kcal/mol) (default)
-m		(MSA) MSA file format (Force: Hartree/Bohr, Dist: Ang, Eng: Hartree)
-r		(Raw) Raw file format. For testing only. (Force: Hartree/Bohr, Dist: Bohr, Eng: Hartree) 

Input filenames and output filenames will be ignored if the -d option is used. All .log files in the 
directory will be parsed and their output will be written to a file corresponding to the parent filename
with the .xyz extension.

It is important to note that this script was written with BOMD AM1 trajectories
in mind. If you are finding that it does not work as expected for a Gaussian job
using a different method or level of theory you can try to modify the script.
Otherwise, please email me a copy of the script that you are using along with the output file
it is not working correctly with, and I will try to modify the script to work for your job as
soon as possible.

Important: There seems to be a small issue with restarting trajectories from a failed previous run,
where although the time printed in the log file as being 0.0000fs, but the geometry is different
from the orientation input in the log file. I am not sure if this is an issue with Gaussian itself
or Gaussview, where the input gjf was generated, but I am not sure which value is correct or which forces coerrespond 
correctly with the first step in these cases. If all other points match the log file in such a job,
I would recommend manually removing the first step in the xyz file due to this uncertainty.
I have not observed this issue when starting a trajectory from the script designed to generate 
random velocities. Again, gaussian log files can be somewhat lengthy and sometimes inconsistent,
and my code is defintely not infailable. Be sure to always verify at least a few points,
especially recalculated points to ensure that you are using valid data for training.
____________________________________________________________________________________________________________________________________________________________________________
Questions:
Always feel free to shoot me an email at the address above. I will do my best to help you.

