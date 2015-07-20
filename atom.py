#atom.py by Nigel S. Michki; part of nmwizConvertor.py
#Defines the Atom data type and any necessary functions to operate on its data.

from mode import Mode

class Atom(object):
    def __init__(self):
        self.resID = ""
        self.atomName = ""
        self.resName = ""
        self.coordinates = ["0.0" ,"0.0" ,"0.0"]
        self.bFactor = ""
        self.tag = ""   #Last column of .pdb file, usually MAIN or SOLV
        self.modes = []

    def printCoordinates(self):
        return (str(self.coordinates[0]) + " " + str(self.coordinates[1]) 
                + " " + str(self.coordinates[2])) 

    def printMode(self, modeNumber):
        return (self.modes[modeNumber-1]).printMode()

