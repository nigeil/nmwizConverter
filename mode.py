#mode.py by Nigel S. Michki; part of nmwizConvertor.py
#Defines the Mode data type and necessary functions to operate on its data.
#A mode consists of a corresponding atom, frequency, and 3-tuple of doubles
#which correspond to changes in position from the coordinates of the atom. 

class Mode(object):
    def __init__(self):
        self.number = "1"
        self.frequency = "1.0"
        self.atomNumber = "1"
        self.vector = ["0.0", "0.0", "0.0"]

    def printMode(self):
        return (str(self.vector[0]) + " " + str(self.vector[1])
                + " " + str(self.vector[2]))
