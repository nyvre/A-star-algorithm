import tkinter as tk

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
        print('Wystartowano algorytm')


guiManager = GuiManager()
guiManager.start()

