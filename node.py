import math
from enum import Enum

class Status(Enum):
    NOT_CHECKED = 0
    OBSTACLE = 1
    OPENED = 2
    CLOSED = 3

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.status = Status.NOT_CHECKED
        self.parentNode = None

    def getDistance(self, otherNode):
        totalDistance = 0
        disX = abs(self.x - otherNode.x)
        disY = abs(self.y - otherNode.y)
        disDiag = min(disX, disY)
        disStraight = abs(disX - disY)
        totalDistance = disDiag * math.sqrt(2) + disStraight
        return totalDistance

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status
        
    def getG(self):
        return self.g

    def getH(self):
        return self.h

    def setG(self, g):
        self.g = g
        self.updateF()

    def setH(self, endNode):
        self.h = self.getDistance(endNode)
        self.updateF()

    def setParent(self, parentNode):
        self.parentNode = parentNode

    def updateF(self):
        self.f = self.h + self.g

    def __eq__(self, otherNode):
        return self.x == otherNode.x and self.y == otherNode.y

    def __lt__(self, otherNode):
        return self.f > otherNode.f

    def __str__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + '] g: ' + str(self.g) + ' h: ' + str(self.h) + ' f: ' + str(self.f)