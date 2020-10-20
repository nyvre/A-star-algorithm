import tkinter as tk
from tkinter import messagebox
import math
import time
import threading
from datetime import datetime

class GuiManager:
    def __init__(self, master):
        self.master = master
        self.obstacleGrid = [[ False for y in range(15)] for x in range(15)]
        self.isStart = False
        self.isEnd = False
        self.startNode = [None, None]
        self.endNode = [None, None]
        self.path = []
        

    def start(self):
        self.board = tk.Canvas(self.master, width = 450, height = 450, highlightthickness=1, highlightbackground="black")
        self.resetGrid(None)
        self.board.pack(side = tk.TOP)

        initialConditionsButtonsFrame = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        initialConditionsButtonsFrame.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        createStartButton = tk.Button(initialConditionsButtonsFrame, text = 'Set start')
        createEndButton = tk.Button(initialConditionsButtonsFrame, text = 'Set end')
        resetGridButton = tk.Button(initialConditionsButtonsFrame, text = 'Reset grid')
        createStartButton.pack(side = tk.TOP, fill = tk.X)
        createEndButton.pack(side = tk.TOP, fill = tk.X)
        resetGridButton.pack(side = tk.TOP, fill = tk.X)

        startAlgorithmFrame = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        startAlgorithmFrame.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        findPathButton = tk.Button(startAlgorithmFrame, text = 'Find path')
        findPathButton.pack(fill=tk.BOTH, expand=True)

        algorithmStepFrame = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        algorithmStepFrame.pack(fill=tk.BOTH, expand=True, side = tk.LEFT)
        algorithmStepLabel = tk.Label(algorithmStepFrame, text = "Algorithm step time [s]")
        self.stepSlider = tk.Scale(algorithmStepFrame, from_=0, to=2, resolution = 0.1, orient=tk.HORIZONTAL)
        algorithmStepLabel.pack(fill=tk.BOTH, expand=True)
        self.stepSlider.pack(side = tk.BOTTOM)
        createStartButton.bind('<Button-1>', self.createStartNode)
        createEndButton.bind('<Button-1>', self.createEndNode)
        findPathButton.bind('<Button-1>', self.startAlgorithm)
        resetGridButton.bind('<Button-1>', self.resetGrid)
        self.board.bind('<Button-1>', self.changeNodeStatus)

    def resetGrid(self, event):
        self.startNode = [None, None]
        self.endNode = [None, None]
        self.obstacleGrid = [[ False for y in range(15)] for x in range(15)]
        for i in range(15):
            self.board.create_line(0, i*30, 451, i*30, fill = 'black')
            self.board.create_line(i*30, 0, i*30, 451, fill = 'black')

        for i in range(15):
            for j in range(15):
                self.board.create_rectangle(i*30, j*30, i*30 + 30, j*30 + 30, fill = 'white')
        
    def changeNodeStatus(self, event):
        pressedNode = [int(event.x/30), int(event.y/30)]
        if self.isStart == True:
            if self.obstacleGrid[pressedNode[0]][pressedNode[1]] == True:
                return
            if self.startNode[0] != None and self.startNode[1] != None:
                self.board.create_rectangle(self.startNode[0]*30, self.startNode[1]*30, self.startNode[0]*30 + 30, self.startNode[1]*30 + 30, fill = 'white')
            self.board.create_text(pressedNode[0]*30 + 15, pressedNode[1]*30 + 15, text = "START", font=('Arial', 6))
            self.startNode = pressedNode
            self.isStart = False
        elif self.isEnd == True:
            if self.obstacleGrid[pressedNode[0]][pressedNode[1]] == True:
                return
            if self.endNode[0] != None and self.endNode[1] != None:
                self.board.create_rectangle(self.endNode[0]*30, self.endNode[1]*30, self.endNode[0]*30 + 30, self.endNode[1]*30 + 30, fill = 'white')
            self.board.create_text(pressedNode[0]*30 + 15, pressedNode[1]*30 + 15, text = "END", font=('Arial', 6))
            self.endNode = pressedNode
            self.isEnd = False
        else:
            if (pressedNode == self.startNode or pressedNode == self.endNode):
                return
            if self.obstacleGrid[pressedNode[0]][pressedNode[1]] == False:
                self.board.create_rectangle(pressedNode[0]*30, pressedNode[1]*30, pressedNode[0]*30 + 30, pressedNode[1]*30 + 30, fill = 'dark slate gray')
                self.obstacleGrid[pressedNode[0]][pressedNode[1]] = True
            else:
                self.board.create_rectangle(pressedNode[0]*30, pressedNode[1]*30, pressedNode[0]*30 + 30, pressedNode[1]*30 + 30, fill = 'white')
                self.obstacleGrid[pressedNode[0]][pressedNode[1]] = False

    def createStartNode(self, event):
        self.isStart = True

    def createEndNode(self, event):
        self.isEnd = True

    def startAlgorithm(self, event):
        if self.startNode != [None, None] and self.endNode != [None, None]:
            aStarAlgorithm = AStarAlgorithm(self.master, self.board, self.startNode, self.endNode, self.obstacleGrid, self.stepSlider.get())
            thread = threading.Thread(target = aStarAlgorithm.start)
            thread.start()
        else:
            messagebox.showerror("Error", "Invalid initial conditions")
            return


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parentNode = None

    def getDistance(self, otherNode):
        totalDistance = 0
        disX = abs(self.x - otherNode.x)
        disY = abs(self.y - otherNode.y)
        disDiag = min(disX, disY)
        disStraight = abs(disX - disY)
        totalDistance = disDiag * math.sqrt(2) + disStraight
        return totalDistance
        

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

class AStarAlgorithm:
    def __init__(self, master, visualGrid, startNode, endNode, obstacleGrid, step):
        self.master = master
        self.visualGrid = visualGrid
        self.startNode = Node(startNode[0], startNode[1])
        self.endNode = Node(endNode[0], endNode[1])
        self.obstacleGrid = obstacleGrid
        self.openNodesArray = []
        self.closedNodesArray = []
        self.step = step
        self.finished = threading.Event()
        
    def getNeighbours(self, i, j):
        neighbours = []
        neighbours.append(Node(i - 1, j - 1))
        neighbours.append(Node(i - 1, j))
        neighbours.append(Node(i - 1, j + 1))
        neighbours.append(Node(i, j + 1))
        neighbours.append(Node(i + 1, j + 1))
        neighbours.append(Node(i + 1, j))
        neighbours.append(Node(i + 1, j - 1))
        neighbours.append(Node(i, j - 1))
        neighbours[:] = [neighbour for neighbour in neighbours if neighbour.x >= 0 and neighbour.x <= 14 and neighbour.y >= 0 and neighbour.y <= 14]
        neighbours[:] = [neighbour for neighbour in neighbours if self.obstacleGrid[neighbour.x][neighbour.y] != True]
        for index, neighbour in enumerate(neighbours):
            if neighbour in self.closedNodesArray:
                neighbours[index] = self.closedNodesArray[self.closedNodesArray.index(neighbour)]
            if neighbour in self.openNodesArray:
                neighbours[index] = self.openNodesArray[self.openNodesArray.index(neighbour)]
        return neighbours

    def start(self):
        self.openNodesArray.append(self.startNode)
        self.performSteps()
        self.finished.wait(10000)
        path = self.reconstructPath()
        self.finish(path)

    def performSteps(self):
        self.openNodesArray.sort()

        currentNode = self.openNodesArray.pop()
        print(currentNode)
        if currentNode == self.endNode:
            self.closedNodesArray.append(currentNode)
            self.finished.set()
            return
        currentNodeNeighbours = self.getNeighbours(currentNode.x, currentNode.y)
        for currentNodeNeighbour in currentNodeNeighbours:
            neighbourCurrentCost = currentNode.getG() + currentNode.getDistance(currentNodeNeighbour)
            if currentNodeNeighbour in self.openNodesArray:
                if currentNodeNeighbour.getG() <= neighbourCurrentCost: 
                    continue
                currentNodeNeighbour.setG(neighbourCurrentCost)
                currentNodeNeighbour.setParent(currentNode)
            elif currentNodeNeighbour in self.closedNodesArray:
                if currentNodeNeighbour.getG() <= neighbourCurrentCost: 
                    continue
                currentNodeNeighbour.setG(neighbourCurrentCost)
                currentNodeNeighbour.setParent(currentNode)
                self.openNodesArray.append(currentNodeNeighbour)
                self.closedNodesArray.remove(currentNodeNeighbour)
            else:
                currentNodeNeighbour.setH(self.endNode)
                currentNodeNeighbour.setG(neighbourCurrentCost)
                currentNodeNeighbour.setParent(currentNode)
                self.openNodesArray.append(currentNodeNeighbour)
        self.closedNodesArray.append(currentNode)
        self.drawCurrentState()
        self.master.after(int(self.step*1000), self.performSteps)


    def drawCurrentState(self):
        if self.closedNodesArray:
            for closedNode in self.closedNodesArray:
                if closedNode != self.startNode and closedNode != self.endNode:
                    self.visualGrid.create_rectangle(closedNode.x*30, closedNode.y*30, closedNode.x*30 + 30, closedNode.y*30 + 30, fill = 'DodgerBlue2')
        if self.openNodesArray:
            for openNode in self.openNodesArray:
                if openNode != self.startNode and openNode != self.endNode:
                    self.visualGrid.create_rectangle(openNode.x*30, openNode.y*30, openNode.x*30 + 30, openNode.y*30 + 30, fill = 'DarkOliveGreen3')

    def finish(self, path):
        for node in path:
            self.visualGrid.create_rectangle(node.x*30, node.y*30, node.x*30 + 30, node.y*30 + 30, fill = 'tomato2')


    def reconstructPath(self):
        node = self.endNode
        pathNodes = []
        while self.closedNodesArray[self.closedNodesArray.index(node)].parentNode != self.startNode:
            node = self.closedNodesArray[self.closedNodesArray.index(node)].parentNode
            pathNodes.append(node)
        return pathNodes



root = tk.Tk()           
    
root.title('A* algorithm')
guiManager = GuiManager(root)
guiManager.start()
root.mainloop()

