#!/usr/bin/python
#nmwizConvertor.py by Nigel S. Michki
#usage: nmwizConverter filename1.pdb filename2.out proteinName
#returns: a file in .nmd format which can be read by NormalModeWiz and used
#to generate a series of movies depicting motions for each normal mode in VMD.

#System imports
from __future__ import print_function #Provides python 2 compatability
import sys

#Local (nmwizConverter) imports
from mode import Mode
from atom import Atom

#isInt checks to see that a string translates to an integer.
#This function is needed to correctly parse to mode.out file.
def isInt(inString):
    try:
        int(inString)
        return True
    except ValueError:
        return False

#Check for correct number of command line arguments
if len(sys.argv) != 4:
    print("Error: incorrect number of command line arguments provided.")
    print("Usage: nmwizConverter structure.pdb modes.out name_of_molecule")
    sys.exit(2)

#Global variables 
pdbFilename = sys.argv[1]
modeFilename = sys.argv[2]
proteinName = sys.argv[3]
nmdFilename = proteinName + ".nmd"
atoms = []

###BEGIN HEAVY LIFTING###

#Read .pdb file and create Atom objects with corresponding data from file
with open(pdbFilename) as pdbFile:
    pdbLines = pdbFile.readlines()

for line in pdbLines:
   words = str.split(line)
   if len(words) < 1:
       pass
   elif words[0] == "ATOM":
       newAtom = Atom()
       newAtom.resID = words[1]
       newAtom.atomName = words[2]
       newAtom.resName = words[3]
       newAtom.coordinates = [words[5], words[6], words[7]]
       newAtom.bFactor = words[9]
       newAtom.tag = words[10]
       atoms.append(newAtom)


#Read .out file add corresponding mode data from file to existing Atom objects
##This asssumes a very regular formatting after the first VIBRATION keyword.
##It will produce incorrect output if lines are malformed, or if
##the VIBRATION keyword's first appearance is not directly before mode data.
with open(modeFilename) as modeFile:
    modeLines = modeFile.readlines()

currentModeNumber = 0
currentModeFrequency = 0.0
for line in modeLines:
    words = str.split(line)
    if len(words) < 1:
        pass
    elif words[0] == "VIBRATION":
        currentModeNumber = words[2]
        currentModeFrequency = words[4]
    elif isInt(words[0]) and currentModeNumber != 0 and len(words) == 7: 
        newMode = Mode()
        newMode.number = currentModeNumber
        newMode.frequency = currentModeFrequency
        newMode.atomNumber = words[0]
        newMode.vector = [words[4], words[5], words[6]]
        atoms[int(newMode.atomNumber) - 1].modes.append(newMode)


#Ask user which chains (tags) they want printed to the ouput file, and remove
#atoms with these tags before printing.
tags = set()
for atom in atoms:
    if atom.tag not in tags:
        tags.add(atom.tag)
keepTags = set(tags)

if len(tags) > 1:
    print("More than one chain/tag is present in the .pdb file. They are listed below:")
    for tag in tags:
        print(tag)
    for tag in tags:
        keepMeFlag = input("Keep atoms of chain/tag \"" + tag + "\" in output file? y/n: ")
        if keepMeFlag == 'n' or keepMeFlag == 'N' or keepMeFlag == 'no':
            keepTags.remove(tag)
    keepAtoms = list(atoms)
    for atom in atoms:
        if atom.tag not in keepTags:
            keepAtoms.remove(atom)
    atoms = list(keepAtoms)
if len(keepTags) < 1:
    print("No chains/tags selected for output; exiting.")
    sys.exit(0)

#Assemble data into a list printable strings
printTheseLines = []

printTheseLines.append("nmwiz_load" + " " + proteinName + ".nmd")
printTheseLines.append("name" + " " + proteinName)

atomNames = ""
resNames = ""
resIDs = ""
chainIDs = ""
bFactors = ""
coordinates = ""
for atom in atoms:
    atomNames = atomNames + atom.atomName + " "
    resNames = resNames + atom.resName + " "
    resIDs = resIDs + atom.resID + " "
    chainIDs = chainIDs + atom.tag + " "
    bFactors = bFactors + atom.bFactor + " "
    coordinates = coordinates + atom.printCoordinates() + " "
printTheseLines.append("atomnames" + " " + atomNames)
printTheseLines.append("resnames" + " " + resNames)
printTheseLines.append("resids" + " " + resIDs)
printTheseLines.append("chainids" + " " + chainIDs)
printTheseLines.append("bfactors" + " " + bFactors)
printTheseLines.append("coordinates" + " " + coordinates)

##This is a little tricky; each line containing a mode is formatted as:
##'mode NUMBER [x,y,z] [x1,y1,z1] ...'.
##To get the numbers, grab the mode number from the first atom's list
##of modes and then write 'mode THAT_NUMBER' to as many new printable
##lines as needed. Then to get the coordinates for each line, iterate
##over all of the atoms, then iterate over all of its modes, and print
##the coordinates of each mode in the correct line. 
numberOfLinesBeforeModes = len(printTheseLines)
numberOfModes = len(atoms[0].modes)
for i in range(0, numberOfModes):
    printTheseLines.append("mode" + " " + str(atoms[0].modes[i].number) + " "
                            + str(atoms[0].modes[i].frequency) + " ")
for atom in atoms:
    for mode in atom.modes:
        printTheseLines[numberOfLinesBeforeModes + int(mode.number) - 1] += ( 
            mode.printMode() + " ")

#Write .nmd file with printable strings
with open(nmdFilename, "w") as nmdFile:
    for line in printTheseLines:
        print(line, file=nmdFile)

print("Output written to" + " " + nmdFilename)

###END HEAVY LIFTING###
