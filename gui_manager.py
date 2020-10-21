import tkinter as tk
import threading
from grid import Grid
from node import Node, Status
from a_star_algorithm import AStarAlgorithm

class GuiManager:
    def __init__(self, master):
        self.master = master
        self.obstacleGrid = Grid(15, 15)
        self.isStart = False
        self.isEnd = False
        self.startNode = Node(None, None)
        self.endNode = Node(None, None)
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
        self.startNode = Node(None, None)
        self.endNode = Node(None, None)
        self.obstacleGrid = Grid(15, 15)
        for i in range(15):
            self.board.create_line(0, i*30, 451, i*30, fill = 'black')
            self.board.create_line(i*30, 0, i*30, 451, fill = 'black')

        for i in range(15):
            for j in range(15):
                self.board.create_rectangle(i*30, j*30, i*30 + 30, j*30 + 30, fill = 'white')
        
    def changeNodeStatus(self, event):
        pressedNode = Node(int(event.x/30), int(event.y/30))
        if self.isStart == True:
            if self.obstacleGrid.getNodeStatus(pressedNode) == Status.OBSTACLE:
                return
            if self.startNode != Node(None, None):
                self.drawRectangleOnGrid(self.startNode, 'white')
            self.board.create_text(pressedNode.x*30 + 15, pressedNode.y*30 + 15, text = "START", font=('Arial', 6))
            self.startNode = pressedNode
            self.isStart = False
        elif self.isEnd == True:
            if self.obstacleGrid.getNodeStatus(pressedNode) == Status.OBSTACLE:
                return
            if self.endNode != Node(None, None):
                self.drawRectangleOnGrid(self.endNode, 'white')
            self.board.create_text(pressedNode.x*30 + 15, pressedNode.y*30 + 15, text = "END", font=('Arial', 6))
            self.endNode = pressedNode
            self.isEnd = False
        else:
            if (pressedNode == self.startNode or pressedNode == self.endNode):
                return
            if self.obstacleGrid.getNodeStatus(pressedNode) == Status.NOT_CHECKED:
                self.drawRectangleOnGrid(pressedNode, 'dark slate gray')
                self.obstacleGrid.setNodeStatus(pressedNode, Status.OBSTACLE)
            else:
                self.drawRectangleOnGrid(pressedNode, 'white')
                self.obstacleGrid.setNodeStatus(pressedNode, Status.NOT_CHECKED)

    def drawRectangleOnGrid(self, node, color):
        self.board.create_rectangle(node.x*30, node.y*30, node.x*30 + 30, node.y*30 + 30, fill = color)

    def createStartNode(self, event):
        self.isStart = True

    def createEndNode(self, event):
        self.isEnd = True

    def startAlgorithm(self, event):
        if self.startNode != Node(None, None) and self.endNode != Node(None, None):
            aStarAlgorithm = AStarAlgorithm(self.master, self.board, self.startNode, self.endNode, self.obstacleGrid, self.stepSlider.get())
            thread = threading.Thread(target = aStarAlgorithm.start)
            thread.start()
        else:
            messagebox.showerror("Error", "Invalid initial conditions")
            return