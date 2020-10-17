import tkinter as tk
import math

class GuiManager:
    def __init__(self):
        self.obstacleGrid = [[ False for y in range(15)] for x in range(15)]
        self.isStart = False
        self.isEnd = False
        self.startNode = [None, None]
        self.endNode = [None, None]
        

    def start(self):
        window = tk.Tk()
        self.board = tk.Canvas(window, width = 450, height = 450, highlightthickness=1, highlightbackground="black")
        for i in range(15):
            self.board.create_line(0, i*30, 451, i*30, fill = 'black')
            self.board.create_line(i*30, 0, i*30, 451, fill = 'black')

        for i in range(15):
            for j in range(15):
                self.board.create_rectangle(i*30, j*30, i*30 + 30, j*30 + 30, fill = 'white')
        createStartButton = tk.Button(window, text = 'Set start')
        createEndButton = tk.Button(window, text = 'Set end')
        findPathButton = tk.Button(window, text = 'Find path')
        self.board.pack()
        createStartButton.pack()
        createEndButton.pack()
        findPathButton.pack()
        createStartButton.bind('<Button-1>', self.createStartNode)
        createEndButton.bind('<Button-1>', self.createEndNode)
        findPathButton.bind('<Button-1>', self.startAlgorithm)
        self.board.bind('<Button-1>', self.changeNodeStatus)
        window.mainloop()
        
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
                self.board.create_rectangle(pressedNode[0]*30, pressedNode[1]*30, pressedNode[0]*30 + 30, pressedNode[1]*30 + 30, fill = 'black')
                self.obstacleGrid[pressedNode[0]][pressedNode[1]] = True
            else:
                self.board.create_rectangle(pressedNode[0]*30, pressedNode[1]*30, pressedNode[0]*30 + 30, pressedNode[1]*30 + 30, fill = 'white')
                self.obstacleGrid[pressedNode[0]][pressedNode[1]] = False

    def createStartNode(self, event):
        self.isStart = True

    def createEndNode(self, event):
        self.isEnd = True

    def startAlgorithm(self, event):
        aStarAlgorithm = AStarAlgorithm(self.board, self.startNode, self.endNode, self.obstacleGrid)

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

    def getF(self):
        return self.f

    def updateF(self):
        self.f = self.h + self.g

    def __eq__(self, otherNode):
        return self.x == otherNode.x and self.y == otherNode.y

    def __lt__(self, otherNode):
        return self.f > otherNode.f

    def __str__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + '] g: ' + str(self.g) + ' h: ' + str(self.h) + ' f: ' + str(self.f)

class AStarAlgorithm:
    def __init__(self, visualGrid, startNode, endNode, obstacleGrid):
        self.visualGrid = visualGrid
        self.startNode = Node(startNode[0], startNode[1])
        self.endNode = Node(endNode[0], endNode[1])
        self.obstacleGrid = obstacleGrid
        self.openNodesArray = []
        self.closedNodesArray = []
        self.start()
        
    def getNeighbours(self, i, j):
        neighbours = []
        if i > 0 and j > 0:
            neighbours.append(Node(i - 1, j - 1))
        if i > 0:
            neighbours.append(Node(i - 1, j))
        if i > 0 and j < 14:
            neighbours.append(Node(i - 1, j + 1))
        if j < 14:
            neighbours.append(Node(i, j + 1))
        if i < 14 and j < 14:
            neighbours.append(Node(i + 1, j + 1))
        if i < 14:
            neighbours.append(Node(i + 1, j))
        if i < 14 and j > 0:
            neighbours.append(Node(i + 1, j - 1))
        if j > 0:
            neighbours.append(Node(i, j - 1))
        neighbours[:] = [neighbour for neighbour in neighbours if self.obstacleGrid[neighbour.x][neighbour.y] != True]
        return neighbours

    def start(self):
        self.openNodesArray.append(self.startNode)
        while(self.openNodesArray):
            self.openNodesArray.sort()
            print("lista")
            for node in self.openNodesArray:
                print(node)
            print("end lista")
            currentNode = self.openNodesArray.pop()
            print(currentNode)
            if currentNode == self.endNode:
                self.closedNodesArray.append(currentNode)
                break
            currentNodeNeighbours = self.getNeighbours(currentNode.x, currentNode.y)
            for currentNodeNeighbour in currentNodeNeighbours:
                if currentNodeNeighbour in self.openNodesArray:
                    print("pierwszy wszed")
                    if currentNodeNeighbour.getG() <= currentNode.getF(): 
                        continue
                elif currentNodeNeighbour in self.closedNodesArray:
                    print("drigu wszed")
                    if currentNodeNeighbour.getG() <= currentNode.getF(): 
                        continue
                    self.openNodesArray.remove(currentNodeNeighbour)
                else:
                    print("czeci wszed")
                    currentNodeNeighbour.setH(self.endNode)
                    currentNodeNeighbour.setG(currentNode.f + currentNodeNeighbour.getDistance(currentNode))
                    currentNodeNeighbour.setParent(currentNode)
                    self.openNodesArray.append(currentNodeNeighbour)
            self.closedNodesArray.append(currentNode)
        if currentNode == self.endNode:
            print("GREAT SUCCESS")
            self.reconstructPath()

    def reconstructPath(self):
        node = self.endNode
        while node != self.startNode:
            print(node)
            node = self.closedNodesArray[self.closedNodesArray.index(node)].parentNode
            self.visualGrid.create_rectangle(node.x*30, node.y*30, node.x*30 + 30, node.y*30 + 30, fill = 'red')




            
    
guiManager = GuiManager()
guiManager.start()

