import numpy as np
from helperFunction import *

def EuclideanDistance(x1,y1,x2,y2):
    return np.sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def ManhattanDistance(x1,y1,x2,y2):
    return (np.abs(x1 - x2) + np.abs(y1 - y2))
    
def missPlace(x1,y1,x2,y2):
    if x1 == x2 and y1 == y2:
        return 0
    return 1
    