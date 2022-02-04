import time
import os, psutil
pid = os.getpid()

# This class represent the node in A* Search for 15 Puzzle Problem
class Node:
    # This method executes when Node class is instantiated (a constructor method), takes its current state and heuristic function as an argument
    def __init__(self, currentState, heuristic):
        # binding variables to the object
        self.children = []
        self.state = []
        self.parent = None
        self.moves = ''
        self.state = currentState
        self.indexOfZero = self.state.index(0)
        self.cost = 0
        self.totalCost = 0
        # assign which heuristic to calculate the evaluation function
        self.heuristic = heuristic
        # creating a hashable item from list
        self.map = '|'.join(str(item) for item in self.state)

    # Set Total Cost
    def setTotalCost(self):
        # Calculating the evaluation function as totalCost  i.e. f(n) = g(n) + h(n)
        self.totalCost = self.cost + self.heuristic(self.state, self.goalState, self.columns)


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


# This method is responsible of creating children nodes of the node passed and assign them the new state
def createChildren(node, newState, move):
    child = Node(newState, node.heuristic)
    node.children.append(child)
    child.parent = node
    # update the move of child by appending moves of parent so that path to goal can be traced
    child.moves = node.moves + move
    # incrementing the cost of children by 1 (Assumption: each action cost 1 unit of cost)
    child.cost = node.cost + 1
    # calulate the evaluation function to set the Total Cost i.e. f(n) = g(n) + h(n)
    child.setTotalCost()


# This method returns the total of manhattan distance of all tiles to their goal position
def manhattanDistanceHeuristic(state, goalState, gameSize):
    totalManhattanDistance = 0
    for index in range(0, len(state)):
        item = state[index]
        if(item == 0):
            continue
        indexInGoal = goalState.index(item)
        diffRow = abs(index // gameSize - indexInGoal // gameSize)
        diffCol = abs(index % gameSize - indexInGoal % gameSize)
        totalManhattanDistance += diffRow + diffCol
    return totalManhattanDistance


# This method returns the number of misplaced tiles in the puzzle as compared to its goal state
def misplacedTilesHeuristic(state, goalState, gameSize):
    totalMisplacedTiles = 0
    for index in range(0, len(state)):
        item = state[index]
        if(item == 0):
            continue
        indexInGoal = goalState.index(item)
        if(index != indexInGoal):
            totalMisplacedTiles += 1
    return totalMisplacedTiles


# Defining Heuristics and storing reference to particular methods
availableHeuristics = {
    "h1": misplacedTilesHeuristic,
    "h2": manhattanDistanceHeuristic
}


# This method makes the python list a priority queue, only the node with lowest cost (estimated) to goal is returned from the frontier
def getPriorityNode(nodeList):
    lowestCost = nodeList[0].totalCost
    lowestCostIndex = 0
    for index in range(0, len(nodeList)):
        node = nodeList[index]
        if(node.totalCost < lowestCost):
            lowestCost = node.totalCost
            lowestCostIndex = index
    lowestCostNode = nodeList[lowestCostIndex]
    # lowest cost node is popped off the frontier
    nodeList.remove(lowestCostNode)
    return lowestCostNode


# This function checks whether the node's state is part of the hashset "setToCheck"
def checkNodeInSet(setToCheck, node):
    return node.map in setToCheck


# This method is the implementation of A* Search Algorithm
# First argument is the rootNode
# Second argument is the goal state
def AStarSearch(rootNode, goalState):
    rootNode.setTotalCost()
    goalStateMapString = '|'.join(str(item) for item in goalState)
    # Frontier a priority queue (represented by a list)
    frontier = []

    # Hashset for checking reached nodes
    reached = set()

    #stores number of nodes expanded
    nodesExpanded = 0

    # adding root node to the frontier
    frontier.append(rootNode)

    # Initially, the solution (or result) is set to False
    solution = None

    while(len(frontier) > 0 and solution == None):
        # Functioning of priority queue (also pops out the lowest cost node from frontier)
        currentNode = getPriorityNode(frontier)

        # adding that node to reached set
        reached.add(currentNode.map)

        # Check if goal is achieved
        if(isSameState(currentNode, goalStateMapString)):
            solution = currentNode
            break

        # expanding the node
        expandState(currentNode)
        #incrementing the node expansion counter
        nodesExpanded += 1
        
        for i in range(0, len(currentNode.children)):
            # Check for repeated states, check if whether the child node was already traversed before or not
            if(not(checkNodeInSet(reached, currentNode.children[i]))):
                frontier.append(currentNode.children[i])      

    return [solution, nodesExpanded]


# Methods used to execute the A* Search for 15 Puzzle Problem
# Takes initial state (problem) as first argument
def fifteenPuzzle(initialState):
    # Set columns for 15 puzzle
    Node.columns = 4
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  
    Node.goalState = goalState

    # A* Search with Misplaced tiles as a Heuristic
    [solution1, nodesExpanded1] = AStarSearch(Node(initialState, availableHeuristics["h1"]), goalState)
    if(solution1):
        print('Moves to reach result (for A* Search with Misplaced Tiles as a heuristic): ', solution1.moves)
    else:
        print('no solution found for A* Search with Misplaced Tiles as a heuristic')
    
    # Print how many nodes have been expanded
    print('Nodes expanded for (A* Search with Misplaced Tiles as a heuristic): ', nodesExpanded1)

    # A* Search with Manhattan distance as a Heuristic
    [solution2, nodesExpanded2] = AStarSearch(Node(initialState, availableHeuristics["h2"]), goalState)
    if(solution2):
        print('Moves to reach result (for A* Search with Manhattan Distance as a heuristic): ', solution2.moves)
    else:
        print('no solution found for A* Search with Manhattan Distance as a heuristic')
    
    # Print how many nodes have been expanded
    print('Nodes expanded (for A* Search with Manhattan Distance as a heuristic): ', nodesExpanded2)


# Start time
start = time.time()
# Create a process
ps = psutil.Process(pid)

initialState = [1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15]
# start the search for goal
fifteenPuzzle(initialState)

# Print time taken by program (end - start)
print('Time Taken: ', (time.time() - start), ' seconds')
memoryUse = ps.memory_info().vms/1024 
# Print the memory used by program
print('Memory Used: ', memoryUse, ' kB')