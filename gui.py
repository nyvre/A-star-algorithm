import tkinter as tk

def changeNodeStatus(event):
    global obstacleGrid, isStart, isEnd, startNode, endNode
    if isStart == True:
        if obstacleGrid[int(event.x/30)][int(event.y/30)] == True:
            return
        if startNode[0] != None and startNode[1] != None:
            board.create_rectangle(startNode[0]*30, startNode[1]*30, startNode[0]*30 + 30, startNode[1]*30 + 30, fill = 'white')
        board.create_text(int(event.x/30)*30 + 15, int(event.y/30)*30 + 15, text = "START", font=('Arial', 6))
        startNode = [int(event.x/30), int(event.y/30)]
        isStart = False
    elif isEnd == True:
        if obstacleGrid[int(event.x/30)][int(event.y/30)] == True:
            return
        if endNode[0] != None and endNode[1] != None:
            board.create_rectangle(endNode[0]*30, endNode[1]*30, endNode[0]*30 + 30, endNode[1]*30 + 30, fill = 'white')
        board.create_text(int(event.x/30)*30 + 15, int(event.y/30)*30 + 15, text = "END", font=('Arial', 6))
        endNode = [int(event.x/30), int(event.y/30)]
        isEnd = False
    else:
        if (int(event.x/30) == startNode[0] and int(event.y/30) == startNode[1]) or (int(event.x/30) == endNode[0] and int(event.y/30) == endNode[1]):
            return
        if obstacleGrid[int(event.x/30)][int(event.y/30)] == False:
            board.create_rectangle(int(event.x/30)*30, int(event.y/30)*30, int(event.x/30)*30 + 30, int(event.y/30)*30 + 30, fill = 'black')
            obstacleGrid[int(event.x/30)][int(event.y/30)] = True
        else:
            board.create_rectangle(int(event.x/30)*30, int(event.y/30)*30, int(event.x/30)*30 + 30, int(event.y/30)*30 + 30, fill = 'white')
            obstacleGrid[int(event.x/30)][int(event.y/30)] = False

def createStartNode(event):
    global isStart
    isStart = True

def createEndNode(event):
    global isEnd
    isEnd = True

def startAlgorithm(event):
    print('Wystartowano algorytm')

class 
isStart = False
isEnd = False
startNode = [None, None]
endNode = [None, None]
window = tk.Tk()
obstacleGrid = [[ False for y in range(15)]
        for x in range(15)]

board = tk.Canvas(window, width = 450, height = 450, highlightthickness=1, highlightbackground="black")
for i in range(15):
    board.create_line(0, i*30, 451, i*30, fill = 'black')
    board.create_line(i*30, 0, i*30, 451, fill = 'black')

for i in range(15):
    for j in range(15):
        board.create_rectangle(i*30, j*30, i*30 + 30, j*30 + 30, fill = 'white')
createStartButton = tk.Button(window, text = 'Set start')
createEndButton = tk.Button(window, text = 'Set end')
findPathButton = tk.Button(window, text = 'Find path')
board.pack()
createStartButton.pack()
createEndButton.pack()
findPathButton.pack()
createStartButton.bind('<Button-1>', createStartNode)
createEndButton.bind('<Button-1>', createEndNode)
findPathButton.bind('<Button-1>', startAlgorithm)
board.bind('<Button-1>', changeNodeStatus)

window.mainloop()

