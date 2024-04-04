import matplotlib.pyplot as plt
import networkx as nx
from enum import Enum
import matplotlib.pyplot as plt
import math

# class syntax
class Child(Enum):
    NE = 0
    SE = 1
    SW = 2
    NW = 3

class Neighbor(Enum):
    N = 0
    E = 1
    S = 2
    W = 3        

class QuadMaze():
    parent: 'QuadMaze'
    childDir: Child
    centerPosition: tuple

    level: int
    children: dict
    neighbors: dict

    def __init__(self, parent:'QuadMaze' = None, childDir:Child = None):
        self.parent = parent

        self.childDir = childDir
        
        # Init root or calculate child attributes based on parent
        if self.parent == None:
            self.level = 0
            self.centerPosition = (0.0, 0.0)
        else:
            self.level = self.parent.getLevel() + 1
            divisor = 2**self.level
            match childDir:
                case Child.NE:
                    self.centerPosition = ( (parent.centerPosition[0] + (10.0 / divisor)), 
                                            (parent.centerPosition[1] + (10.0 / divisor)) )
                case Child.SE:
                    self.centerPosition = ( (parent.centerPosition[0] + (10.0 / divisor)),
                                            (parent.centerPosition[1] - (10.0 / divisor)) )
                case Child.SW:
                    self.centerPosition = ( (parent.centerPosition[0] - (10.0 / divisor)),
                                            (parent.centerPosition[1] - (10.0 / divisor)) )
                case Child.NW:
                    self.centerPosition = ( (parent.centerPosition[0] - (10.0 / divisor)),
                                            (parent.centerPosition[1] + (10.0 / divisor)) )

        self.children = {Child.NE : None,
                    Child.SE : None,
                    Child.SW : None,
                    Child.NW : None}
        self.neighbors = {Neighbor.N : None,
                     Neighbor.E : None,
                     Neighbor.S : None,
                     Neighbor.W : None}

    def getLevel(self) -> int:
        return self.level
    
    def getCenterPosition(self) -> tuple:
        return self.centerPosition

    def getChild(self, dir:Child) -> 'QuadMaze':
        return self.children[dir]
    
    def getNeighbor(self, dir:Neighbor) -> 'QuadMaze':
        return self.neighbors[dir]

    # Recursively generates children on each level of the tree.
    # Returns the total number of LEAVES (nodes with no children) in the tree
    def generateChildren(self, levels:int) -> int:

        #print("Generating children with level = ", levels)

        # Short circuit if no more levels should be generated
        if levels == 0:
            global leaves
            leaves[self.getCenterPosition()] = self #TODO: REMOVE THIS
            return 1
        
        # Create 4 children, then return the result of calling this function on them
        total = 0
        for dir in Child:
            self.children[dir] = QuadMaze(self, dir)
            total += self.children[dir].generateChildren(levels-1)

        return total

    # Recursively calculates neighbors in cardinal directions for each node in the tree
    # Should only be called from root node of tree, as it assumes that a node with a parent has neighbors
    def calculateNeighbors(self) -> None:

        # If this node has a parent, then it has some neighbors
        if self.level != 0:
            match(self.childDir):
                case Child.NE:
                    # Same Parent
                    self.neighbors[Neighbor.S] = self.parent.getChild(Child.SE)
                    self.neighbors[Neighbor.W] = self.parent.getChild(Child.NW)

                    # Different Parent
                    neighbor = self.parent.getNeighbor(Neighbor.N)
                    if neighbor != None:
                        self.neighbors[Neighbor.N] = neighbor.getChild(Child.SE)
                    neighbor = self.parent.getNeighbor(Neighbor.E)
                    if neighbor != None:
                        self.neighbors[Neighbor.E] = neighbor.getChild(Child.NW)
                case Child.SE:
                    # Same Parent
                    self.neighbors[Neighbor.N] = self.parent.getChild(Child.NE)
                    self.neighbors[Neighbor.W] = self.parent.getChild(Child.SW)

                    # Different Parent
                    neighbor = self.parent.getNeighbor(Neighbor.S)
                    if neighbor != None:
                        self.neighbors[Neighbor.S] = neighbor.getChild(Child.NE)
                    neighbor = self.parent.getNeighbor(Neighbor.E)
                    if neighbor != None:
                        self.neighbors[Neighbor.E] = neighbor.getChild(Child.SW)
                case Child.SW:
                    # Same Parent
                    self.neighbors[Neighbor.N] = self.parent.getChild(Child.NW)
                    self.neighbors[Neighbor.E] = self.parent.getChild(Child.SE)

                    # Different Parent
                    neighbor = self.parent.getNeighbor(Neighbor.S)
                    if neighbor != None:
                        self.neighbors[Neighbor.S] = neighbor.getChild(Child.NW)
                    neighbor = self.parent.getNeighbor(Neighbor.W)
                    if neighbor != None:
                        self.neighbors[Neighbor.W] = neighbor.getChild(Child.SE)
                case Child.NW:
                    # Same Parent
                    self.neighbors[Neighbor.S] = self.parent.getChild(Child.SW)
                    self.neighbors[Neighbor.E] = self.parent.getChild(Child.NE)

                    # Different Parent
                    neighbor = self.parent.getNeighbor(Neighbor.N)
                    if neighbor != None:
                        self.neighbors[Neighbor.N] = neighbor.getChild(Child.SW)
                    neighbor = self.parent.getNeighbor(Neighbor.W)
                    if neighbor != None:
                        self.neighbors[Neighbor.W] = neighbor.getChild(Child.NE)

        # Tell each child of this node to calculate its neighbors
        for dir in Child:
            if self.children[dir] != None:
                self.children[dir].calculateNeighbors()

        return

LEVELS = 4 #Number of levels of children that the root has
leaves = {} #TODO: Remove this and reference from generateChildren

root = QuadMaze()

print(root.generateChildren(LEVELS), " leaves generated in total.")
root.calculateNeighbors()

# currentNode = root
# for i in range(LEVELS):
#     currentNode = currentNode.getChild(Child.NE)

for key in leaves.keys():
    center:QuadMaze = leaves[key]
    cpos = center.getCenterPosition()
    for dir in Neighbor:
        neighbor:QuadMaze = center.getNeighbor(dir)
        if neighbor != None:
            #Draw a line between this and neighbor
            npos = neighbor.getCenterPosition()
            x = (cpos[0], npos[0])
            y = (cpos[1], npos[1])
            plt.plot(x, y, marker = 'o', color="black")

for key in leaves.keys():
    center:QuadMaze = leaves[key]
    cpos = center.getCenterPosition()
    ppos = center.parent.getCenterPosition()
    x = (cpos[0], ppos[0])
    y = (cpos[1], ppos[1])
    plt.plot(x, y, marker = 'o', color="red")


plt.show()

# print("(", currentNode.getCenterPosition()[0], ", ", currentNode.getCenterPosition()[1], ")")

# while True:
#     d = input()

#     if d == "stop".lower():
#         break

#     dir = getattr(Neighbor, d)

#     if currentNode.getNeighbor(dir) != None:
#         currentNode = currentNode.getNeighbor(dir)
     
#     print("(", currentNode.getCenterPosition()[0], ", ", currentNode.getCenterPosition()[1], ")")

drawn = []

# def drawLinesBetweenNeighbors(startNode:QuadMaze) -> None:
#     global drawn

#     # print("call!")
#     if startNode.getCenterPosition() not in drawn:
#         # print("not in drawn")
#         drawn.append(startNode.getCenterPosition())

#         for dir in Neighbor:
#             # print(dir)
#             neighbor = startNode.getNeighbor(dir)
#             if neighbor != None:
#                 # print("neighbor exists!")
#                 # Draw a line between their centers
#                 if startNode.getChild(Child.NE) == None:
#                     x = (startNode.getCenterPosition()[0], neighbor.getCenterPosition()[0])
#                     y = (startNode.getCenterPosition()[1], neighbor.getCenterPosition()[1])

#                     # print(math.dist(startNode.getCenterPosition(), neighbor.getCenterPosition()))

#                     plt.plot(x, y, marker = 'o')
#                     if neighbor.getCenterPosition() not in drawn:
#                         drawLinesBetweenNeighbors(neighbor)
        
        # for dir in Child:
        #     child = startNode.getChild(dir)
        #     if child != None:
        #         drawLinesBetweenNeighbors(child)

# drawLinesBetweenNeighbors(currentNode)
# plt.show(block=False)

