import sys
import time
import os, psutil
pid = os.getpid()

# This class represent the node in IDA* Search for 15 Puzzle Problem
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
        self.heuristicCost = 0
        # assign which heuristic to calculate the evaluation function
        self.heuristic = heuristic
        # creating a hashable item from list
        self.map = '|'.join(str(item) for item in self.state)

    # Set Total Cost
    def setTotalCost(self):
        # Calculating the evaluation function as totalCost  i.e. f(n) = g(n) + h(n)
        self.totalCost = self.cost + self.heuristic(self.state, self.goalState, self.columns)
        self.heuristicCost = self.heuristic(self.state, self.goalState, self.columns)


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



# This method is the implementation of Iterative Deepening A Star Search
# first argument is the root node
# second argument is the goal state
def IDAStar(rootNode, goalState):
    rootNode.setTotalCost()
    goalStateMapString = '|'.join(str(item) for item in goalState)

    # this will hold the path
    frontier = []

    # holds number of nodes expanded
    nodesExpanded = 0

    #setting up the threshold
    cutOff = rootNode.heuristicCost

    frontier.append(rootNode)

    # keep doing cost limited search until a goal is found
    while(True):
        [result, nodesExpandedInThisTurn] = CostLimitedSearch(frontier, rootNode.cost, cutOff, goalStateMapString)
        nodesExpanded += nodesExpandedInThisTurn
        if(result == "FOUND"):
            return [frontier, cutOff, nodesExpanded]
        if(result == sys.maxsize):
            return ["NOT_FOUND"]
        cutOff = result

# this method performs cost limited search
def CostLimitedSearch(frontier, cost, cutOff, goalStateMapString):
    # set goal to false
    isGoal = False
    nodesExpanded = 0

    # select the last item in frontier
    currentNode = frontier[len(frontier) - 1]

    # total cost
    totalCost = cost + currentNode.heuristicCost
    minimum = 0

    # cut off the seach
    if(totalCost > cutOff):
        return [totalCost, nodesExpanded]
    # if goal found then return
    if(isSameState(currentNode, goalStateMapString)):
        isGoal = True
        return ["FOUND", nodesExpanded]
    # expand node if not already expanded
    if(len(currentNode.children) == 0):
        # not expanded
        expandState(currentNode)
        nodesExpanded += 1
    
    # check in all child nodes if node with minimum cost exceeding the cutoff
    for child in currentNode.children:
        if(not(checkNodeInPath(child, frontier))):
            frontier.append(child)
            [t, nexp] = CostLimitedSearch(frontier, cost + costFunc(currentNode, child), cutOff, goalStateMapString)
            nodesExpanded += nexp
            if(t == "FOUND"):
                return ["FOUND", nodesExpanded]
            if(t < minimum):
                minimum = t
            frontier.pop()

    return [minimum, nodesExpanded]

# This method returns cost from Node1 to Node2
def costFunc(node1, node2):
    return node2.cost - node1.cost

# This method checks Node 
def checkNodeInPath(node, path):
    isInPath = False
    for currentNode in path:
        if(node.map == currentNode.map):
            isInPath = True
            break
    return isInPath


# Methods used to execute the IDA* Search for 15 Puzzle Problem
# Takes initial state (problem) as first argument
def fifteenPuzzle(initialState):
    # Set columns for 15 puzzle
    Node.columns = 4
    goalState = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]  
    Node.goalState = goalState

    # IDA* Search with Manhattan Distance as a Heuristic
    [path1, pathCost1, nodesExpanded1] = IDAStar(Node(initialState, manhattanDistanceHeuristic), goalState)
    if(path1 != "NOT_FOUND"):
        print('Moves to reach result (for IDA* Search with Manhattan Distance as a heuristic): ', path1[len(path1) - 1].moves)
    else:
        print('no solution found for IDA* Search with Manhattan Distance as a heuristic')
    
    # Print how many nodes have been expanded
    print('Nodes expanded for (IDA* Search with Manhattan Distance as a heuristic): ', nodesExpanded1)


    # IDA* Search with with Misplaced Tiles as a Heuristic
    [path2, pathCost2, nodesExpanded2] = IDAStar(Node(initialState, misplacedTilesHeuristic), goalState)
    if(path2 != "NOT_FOUND"):
        print('Moves to reach result (for IDA* Search with Misplaced Tiles as a heuristic): ', path2[len(path2) - 1].moves)
    else:
        print('no solution found for IDA* Search with Misplaced Tiles as a heuristic')
    
    # Print how many nodes have been expanded
    print('Nodes expanded for (IDA* Search with Misplaced Tiles as a heuristic): ', nodesExpanded2)


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
# Print the memory used by program`
print('Memory Used: ', memoryUse, ' kB')