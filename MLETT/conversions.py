import math

import numpy as np

#Per official documentation, Gaussian outputs in Angstroms for distances, Hartrees for energy, and Hartrees/Bohr for force 
#while sGDML assumes Angstroms, kcal/mol, and kcal/(mol*ang)
#MSA uses Hartrees/Bohr for gradient and Hartree for energies, but input geometry needs to be in Ang
#This section defines necessary constants for converting between the two values
ANG_PER_BOHR = 0.52917721092
#0.52917721092 Angstrom / Bohr Radius per CRC Handbook of Chemistry and Physics 93rd Edition
HART_PER_KJ = 4.35974434 * 10**-21
#4.35974434 * 10 ^ -21 Hartree / 1 kiloJoule per CRC Handbook of Chemistry and Physics 93rd Edition
AVOGADRO =  6.02214129 * 10 ** 23
#6.02214129 obj / 1 mole per CRC Handbook of Chemistry and Physics 93rd Edition
KJMOL_PER_KCALMOL = 4.184 
#4.184 kiloJoule/mole (thermochemical)/ 1 kilocalorie/mole per National Institute of Science and Technology (NIST) Physical Measurement Laboratory
KCALMOL_PER_HART = HART_PER_KJ * AVOGADRO / KJMOL_PER_KCALMOL
#approximately 627.5094742771939 kilocalorie/mole / 1 hartree 
KCALMOLANG_PER_HARTBOHR = KCALMOL_PER_HART/ANG_PER_BOHR
#approximately 1185.82105 kilocalorie/(mole*ang) / 1 hartree/bohr 


AU = { #Atomic Units 
    "eng":"hart",
    "force":"hart/bohr", 
    "dist":"bohr"
}

SGDML = { #SGDML Standard
    "eng":"kcal/mol",
    "force":"kcal/mol/ang",
    "dist":'ang'
}

MSA = {
    "eng":"hart",
    "force":"hart/bohr",
    'dist':'ang' 
}


SGDML_CONVERSIONS = {
                'dist':ANG_PER_BOHR, #Conversion to angstrom from bohr
                'eng':KCALMOL_PER_HART, #Conversion to kcal/mol from hartree
                'force':(-1 * KCALMOLANG_PER_HARTBOHR), #Conversion to''kcal/mol*ang from hartree/bohr * -1 to convert from gradient to force
                'units':SGDML
                }
 
MSA_CONVERSIONS = {
                'dist':ANG_PER_BOHR, #Conversion to angstrom from bohr
                'units':MSA
                }

RAW_CONVERSIONS = {
}

ATOMIC_NUMBERS_TO_SYM = {
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