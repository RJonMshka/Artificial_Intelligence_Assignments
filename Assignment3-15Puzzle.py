# Importing dependencies
import time
import os, psutil
pid = os.getpid()


# This class represent the node in BFS for 15 Puzzle Problem
class Node:
    
    # This method executes when Node class is instantiated (a constructor method), takes argument as a state and number of columns (4 for 15 puzzle)
    def __init__(self, currentState, columns):

        # binding variables to the object
        self.columns = columns
        self.children = []
        self.state = []
        self.parent = None
        self.moves = ''
        self.state = currentState
        self.indexOfZero = 0;
        # find the index of 0 in current state of puzzle
        self.setZeroIndex()
        # creating a hashable item from list
        self.map = ''.join(str(item) for item in self.state)

    # override the __eq__ method for Node class
    def __eq__(self, nodeToCompare):
        return self.map == nodeToCompare.map

    # This method finds the index of 0 in current state and sets a variables
    def setZeroIndex(self):
        for i in range(0, len(self.state)):
            if(self.state[i] == 0):
                self.indexOfZero = i
                break

    # This method is responsible of creating children nodes of current Node
    def createChildren(self, newState, move):
        child = Node(newState, self.columns)
        self.children.append(child)
        child.parent = self
        # update the move of child by appending moves of parent so that path to goal can be traced
        child.moves = child.parent.moves + move

    # This method check if the passed state is exactly same as Node's current state
    def isSameState(self, stateToCompare):
        isSame = True
        for i in range(0, len(self.state)):
            if(self.state[i] != stateToCompare[i]):
                isSame = False
                break
        return isSame

    # This method moves the position of 0 to left and create child node
    def moveLeft(self):
        if(self.indexOfZero % self.columns > 0):
            tempState = self.state.copy()
            tempState[self.indexOfZero], tempState[self.indexOfZero - 1] = tempState[self.indexOfZero - 1], tempState[self.indexOfZero]

            # Create children with move L (Left)
            self.createChildren(tempState, 'L')

    # This method moves the position of 0 to right and create child node
    def moveRight(self):
        if(self.indexOfZero % self.columns < self.columns - 1):
            tempState = self.state.copy()
            tempState[self.indexOfZero], tempState[self.indexOfZero + 1] = tempState[self.indexOfZero + 1], tempState[self.indexOfZero]

            # Create children with move R (Right)
            self.createChildren(tempState, 'R')

    # This method moves the position of 0 to up and create child node
    def moveUp(self):
        if(self.indexOfZero - self.columns >= 0):
            tempState = self.state.copy()
            tempState[self.indexOfZero], tempState[self.indexOfZero - self.columns] = tempState[self.indexOfZero - self.columns], tempState[self.indexOfZero]
            
            # Create children with move U (Up)
            self.createChildren(tempState, 'U')

    # This method moves the position of 0 to down and create child node
    def moveDown(self):
        if(self.indexOfZero + self.columns < len(self.state)):
            tempState = self.state.copy()
            tempState[self.indexOfZero], tempState[self.indexOfZero + self.columns] = tempState[self.indexOfZero + self.columns], tempState[self.indexOfZero]

            # Create children with move D (Down)
            self.createChildren(tempState, 'D')

    # This method expands current by performing every possible set of moves and thus creating children of current Node
    def expandState(self):
        self.moveLeft()
        self.moveRight()
        self.moveUp()
        self.moveDown()



# This function performs Breadth First Search (BFS), returns a list in which first element is the solution or set of moves to reach gaol state from initial state and 2nd argument as number of nodes that have been expanded in the process
def breadthFirstSearch(rootNode, goalState):
    # Moves to reach to goal from initial state
    movesToGoal = ''

    # Frontier (Queue)
    openList = []

    # Hashset for checking traversed nodes (explored)
    closedSet = set()

    # Counter to keep track of how many nodes have been expanded
    nodesExpanded = 0

    # add the root node to the frontier
    openList.append(rootNode)

    goalFound = False
    
    while(len(openList) > 0 and not(goalFound)):
        # Making a FIFO queue
        currentNode = openList[0]
        openList.pop(0)

        # adding the popped node into explored or closed set
        closedSet.add(currentNode.map)

        # Expand the node
        currentNode.expandState()
        # Incrementing the counter
        nodesExpanded = nodesExpanded + 1

        for i in range(0, len(currentNode.children)):
            currentChild = currentNode.children[i]
            if(currentChild.isSameState(goalState)):
                movesToGoal = currentChild.moves
                goalFound = True
                break

            # Check for repeated states, check if whether the child node was already traversed before or not
            if(not(checkNodeInSet(closedSet, currentChild))):
                openList.append(currentChild)      
        
        # If goal is reached, then do not perform any further search
        if(goalFound):
            break

    # Returning the Solution 
    return [movesToGoal, nodesExpanded]



# This function checks whether the node's state is part of the hashset "setToCheck"
def checkNodeInSet(setToCheck, node):
    return node.map in setToCheck



# This function takes initial state as its first argument and performs Breadth First Search to search for goal state
def FifteenPuzzle(intialState):
    # Goal State
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

    # Number of columns in the puzzle
    columns = 4   

    # create root node from initial state 
    rootNode = Node(intialState, columns)

    # Apply, Breadth First Search and get solution in term of moves from initial state to goal state
    [solution, nodesExpanded] = breadthFirstSearch(rootNode, goalState)

    # Check if solution exists
    if(len(solution)):
        print('Moves: ', solution)
    else:
        print('no solution found')
    
    # Print how many nodes have been expanded
    print('Nodes expanded: ', nodesExpanded)



# Start time
start = time.time()

# Start the 15 Puzzle with initial state
FifteenPuzzle([1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15])

# Print time taken by program (end - start)
print('Time Taken: ', (time.time() - start), ' seconds')

# Create a process
ps = psutil.Process(pid)
memoryUse = ps.memory_info().vms/1024

# Print the memory used by program
print('Memory Used: ', memoryUse, ' kB')