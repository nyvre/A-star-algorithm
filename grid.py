from node import Node, Status
class Grid:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.grid = [[ Node(x, y) for y in range(height)] for x in range(width) ]

    def getNodeStatus(self, node):
        return self.grid[node.x][node.y].getStatus()

    def setNodeStatus(self, node, status):
        self.grid[node.x][node.y].setStatus(status)

    def getClosedNodes(self):
        closedNodes = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].getStatus() == Status.CLOSED:
                    closedNodes.append(self.grid[x][y])
        return closedNodes

    def getOpenedNodes(self):
        openedNodes = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].getStatus() == Status.OPENED:
                    openedNodes.append(self.grid[x][y])
        return openedNodes

    def getNeighbours(self, node):
        neighbours = []
        i = node.x
        j = node.y
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x + i > 14 or y + j > 14 or x + i < 0 or y + j < 0:
                    continue
                if not (x == 0 and y == 0) and self.grid[i + x][j + y].getStatus() != Status.OBSTACLE:
                    neighbours.append(self.grid[i + x][j + y])
        neighbours[:] = [neighbour for neighbour in neighbours if neighbour.x >= 0 and neighbour.x < self.width and neighbour.y >= 0 and neighbour.y < self.height]
        return neighbours