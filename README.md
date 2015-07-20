#nmwizConverter
_______
##What does it do?
__
nmwizConverter is a simple script that takes in as command-line arguments:
1. a .pdb file
2. a file containing normal mode data, created using CHARMM
3. the name of the molecule these files pertains to (or any other name really)
The script returns a file in .nmd format which can then be imported directly
into Normal Mode Wizard, a plugin for VMD which allows researchers to
visualize the vibrational modes of molecules. 
See http://prody.csb.pitt.edu/nmwiz/ for information on that plugin.

##Who is it for?
__
Anyone who understands and is interested in the above section!

##How can I use it?
__
This is still in alpha, so there are no frills just yet. 
A basic python installation is the only requirement. Python 2 & 3 both
seem to work, though you'll have better luck with 3 as that's what I am
developing with.
Presently all one needs to do is clone this into their directory of choice
and run the script as follows:
'''
python nmwizconverter.py pdbFilename.pdb modeFilename.out moleculeName
'''
The output file will apear in the directory in which the script was located;
I intend to change this to be a user-defined location soon.

##I've found a bug; what do I do?
__
Create a new issue in the issue tracker for this git repository. I'll get to it
as soon as possible since it's nice to know other people find this script 
useful.

##I want to know more!
__
Check out these sweet websites:
NMWiz - http://prody.csb.pitt.edu/nmwiz/
VMD - http://www.ks.uiuc.edu/Research/vmd/
Markelz research group - http://markelz.physics.buffalo.edu

