import time
import os, psutil
pid = os.getpid()

# This class represent the node in Iterative Deepening Search for 15 Puzzle Problem
class Node:
    # This method executes when Node class is instantiated (a constructor method), takes argument as a state
    def __init__(self, currentState):
        # binding variables to the object
        self.children = []
        self.state = []
        self.parent = None
        self.moves = ''
        self.state = currentState
        # Number of columns in 15 Puzzle are 4
        self.columns = 4
        self.indexOfZero = 0
        self.depth = 0
        # find the index of 0 in current state of puzzle
        setZeroIndex(self)
        # creating a hashable item from list
        self.map = '|'.join(str(item) for item in self.state)


# This method check if the a particular node's current state map (hashable) is same as the state string passed in 2nd argument
def isSameState(node, stateToCompareString):
    return node.map == stateToCompareString


# This method moves the position of 0 to left and create child node from the passed node
def moveLeft(node):
    if(node.indexOfZero % node.columns > 0):
        tempState = node.state.copy()
        tempState[node.indexOfZero], tempState[node.indexOfZero - 1] = tempState[node.indexOfZero - 1], tempState[node.indexOfZero]

        # Create children with move L (Left)
        createChildren(node, tempState, 'L')


# This method moves the position of 0 to right and create child node from the passed node
def moveRight(node):
    if(node.indexOfZero % node.columns < node.columns - 1):
        tempState = node.state.copy()
        tempState[node.indexOfZero], tempState[node.indexOfZero + 1] = tempState[node.indexOfZero + 1], tempState[node.indexOfZero]

        # Create children with move R (Right)
        createChildren(node, tempState, 'R')


# This method moves the position of 0 to up and create child node from the passed node
def moveUp(node):
    if(node.indexOfZero - node.columns >= 0):
        tempState = node.state.copy()
        tempState[node.indexOfZero], tempState[node.indexOfZero - node.columns] = tempState[node.indexOfZero - node.columns], tempState[node.indexOfZero]
        
        # Create children with move U (Up)
        createChildren(node, tempState, 'U')


# This method moves the position of 0 to down and create child node from the passed node
def moveDown(node):
    if(node.indexOfZero + node.columns < len(node.state)):
        tempState = node.state.copy()
        tempState[node.indexOfZero], tempState[node.indexOfZero + node.columns] = tempState[node.indexOfZero + node.columns], tempState[node.indexOfZero]

        # Create children with move D (Down)
        createChildren(node, tempState, 'D')


# This method expands current by performing every possible set of moves and thus creating children of current Node
def expandState(node):
    moveLeft(node)
    moveRight(node)
    moveUp(node)
    moveDown(node)


# This method finds the index of 0 in a node's state
def setZeroIndex(node):
    for i in range(0, len(node.state)):
        if(node.state[i] == 0):
            node.indexOfZero = i
            break


# This method is responsible of creating children nodes of the node passed and assign them the new state
def createChildren(node, newState, move):
    child = Node(newState)
    node.children.append(child)
    child.parent = node
    # update the move of child by appending moves of parent so that path to goal can be traced
    child.moves = node.moves + move
    child.depth = node.depth + 1


# This method detect whether there is a cycle in path of a particular node
def cycleDetected(node):
    currentNode = node
    isCycle = False
    hashSet = set()
    while(currentNode):
        if(currentNode.map in hashSet):
            isCycle = True
            break
        hashSet.add(currentNode.map)
        currentNode = currentNode.parent
    return isCycle


# This method performs Depth Limited Search
# Accepts rootNode as first Argument
# Accepts goalState as 2nd Argument
# Accepts depth limit as 3rd Argument
def depthLimitedSearch(rootNode, goalState, depthLimit):
    # Creating hashable string out of goal state
    goalStateMapString = '|'.join(str(item) for item in goalState)

    # Frontier is represented as LIFO Priority queue (stack) with the help of python lists
    frontier = []

    # Adding root node to frontier
    frontier.append(rootNode)

    # initializing result as Failure
    result = False

    # Count to take care of number of nodes expanded
    nodesExpanded = 0

    while(len(frontier) != 0):
        # Getting the top most item of the stack (LIFO Priority Queue)
        currentNode = frontier[len(frontier) - 1]
        # Removing that node from stack
        frontier.pop()

        # check if the node's state is same as Goal (GOAL CHECK)
        if(isSameState(currentNode, goalStateMapString)):
            result = currentNode
            break
        
        # Limiting the depth
        if(currentNode.depth > depthLimit):
            result = "cutOff"
        # Detect cycle
        elif(~(cycleDetected(currentNode))):
            #expand the node
            expandState(currentNode)
            nodesExpanded = nodesExpanded + 1
            # adding children to frontier
            for child in currentNode.children:
                frontier.append(child)

    # returning the result and number of nodes expanded
    return [result, nodesExpanded]


# This method performs Iterative Deepening Search
# Accepts rootNode as first Argument
# Accepts goalState as 2nd Argument
def iterativeDeepeningSearch(rootNode, goalState):
    depthLimit = 0
    # Count for total number of nodes expanded in all cycles of iterative deepening search
    nodesExpanded = 0
    # loop runs till infinity and only breaks in case of success (found goal state) or for failure
    while(True):
        [result, nodesExpandedInThisTurn] = depthLimitedSearch(rootNode, goalState, depthLimit)
        depthLimit = depthLimit + 1;
        
        nodesExpanded = nodesExpanded + nodesExpandedInThisTurn
        if(result != "cutOff"):
            break
        else:
            # breaking the link of parent with explored nodes to free up the memory as result is not reached
            rootNode.children = []
    
    # returning the result and the total number of nodes expanded
    return [result, nodesExpanded]


# This function takes initial state as its first argument and performs Iterative Deepening Search to search for goal state
def FifteenPuzzle(intialState):
    # Goal State
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  

    # create root node from initial state 
    rootNode = Node(intialState)

    # Apply, Iterative Deepening Search and get solution in term of moves from initial state to goal state
    [result, nodesExpanded] = iterativeDeepeningSearch(rootNode, goalState)

    # Check if solution exists
    if(result):
        print('Moves: ', result.moves)
        print('Nodes Expanded: ', nodesExpanded)
    else:
        print('no solution found')


# Start time
start = time.time()
# Create a process
ps = psutil.Process(pid)

# Start solving the puzzle with supplying the initial state
initialState = [1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15]
FifteenPuzzle(initialState)

# Print time taken by program (end - start)
print('Time Taken: ', (time.time() - start), ' seconds')
memoryUse = ps.memory_info().vms/1024 
# Print the memory used by program
print('Memory Used: ', memoryUse, ' kB')