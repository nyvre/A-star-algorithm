import threading
from node import Status

class AStarAlgorithm:
    def __init__(self, master, visualGrid, startNode, endNode, obstacleGrid, step):
        self.master = master
        self.visualGrid = visualGrid
        self.startNode = startNode
        self.endNode = endNode
        self.grid = obstacleGrid
        self.step = step
        self.finished = threading.Event()
        
    def start(self):
        self.grid.setNodeStatus(self.startNode, Status.OPENED)
        self.performSteps()
        self.finished.wait(10000)
        path = self.reconstructPath()
        self.finish(path)

    def performSteps(self):
        openedNodes = self.grid.getOpenedNodes()
        openedNodes.sort()
        closedNodes = self.grid.getClosedNodes()
        currentNode = openedNodes.pop()
        if currentNode == self.endNode:
            self.grid.setNodeStatus(currentNode, Status.CLOSED)
            self.finished.set()
            return
        currentNodeNeighbours = self.grid.getNeighbours(currentNode)
        for currentNodeNeighbour in currentNodeNeighbours:
            neighbourCurrentCost = currentNode.getG() + currentNode.getDistance(currentNodeNeighbour)
            if currentNodeNeighbour in openedNodes:
                if currentNodeNeighbour.getG() <= neighbourCurrentCost: 
                    continue
            elif currentNodeNeighbour in closedNodes:
                if currentNodeNeighbour.getG() <= neighbourCurrentCost: 
                    continue
                self.grid.setNodeStatus(currentNodeNeighbour, Status.OPENED)
            else:
                self.grid.grid[currentNodeNeighbour.x][currentNodeNeighbour.y].setH(self.endNode)
                self.grid.setNodeStatus(currentNodeNeighbour, Status.OPENED)

            self.grid.grid[currentNodeNeighbour.x][currentNodeNeighbour.y].setG(neighbourCurrentCost)
            self.grid.grid[currentNodeNeighbour.x][currentNodeNeighbour.y].setParent(currentNode)
        self.grid.setNodeStatus(currentNode, Status.CLOSED)
        self.drawCurrentState()
        self.master.after(int(self.step*1000), self.performSteps)


    def drawCurrentState(self):
        closedNodes = self.grid.getClosedNodes()
        openedNodes = self.grid.getOpenedNodes()
        if closedNodes:
            for closedNode in closedNodes:
                if closedNode != self.startNode and closedNode != self.endNode:
                    self.visualGrid.create_rectangle(closedNode.x*30, closedNode.y*30, closedNode.x*30 + 30, closedNode.y*30 + 30, fill = 'DodgerBlue2')
        if openedNodes:
            for openNode in openedNodes:
                if openNode != self.startNode and openNode != self.endNode:
                    self.visualGrid.create_rectangle(openNode.x*30, openNode.y*30, openNode.x*30 + 30, openNode.y*30 + 30, fill = 'DarkOliveGreen3')

    def finish(self, path):
        for node in path:
            self.visualGrid.create_rectangle(node.x*30, node.y*30, node.x*30 + 30, node.y*30 + 30, fill = 'tomato2')


    def reconstructPath(self):
        closedNodes = self.grid.getClosedNodes()
        node = self.endNode
        pathNodes = []
        while closedNodes[closedNodes.index(node)].parentNode != self.startNode:
            node = closedNodes[closedNodes.index(node)].parentNode
            pathNodes.append(node)
        return pathNodes