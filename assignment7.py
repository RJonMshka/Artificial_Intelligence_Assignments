import random

# MDP Class definition
class MDP:

    # MDP constructor accepts states, actions, transition model and reward function
    def __init__(self, states, actions, tModel, rewardFunc):
        self.states = states
        self.actions = actions
        self.tModel = tModel
        self.rewardFunc = rewardFunc


# This method build the states list (representation of grid MDP states)
def buildStates(rows, cols):
    return [[(i // cols)+1 if(i % cols) else (i//cols), (i % cols) if(i % cols) else cols] for i in range(1, (rows * cols) + 1)] 


# This method returns the index of state in states list
def getStateIndex(state, cols):
    [row, col] = state
    return (row - 1) * cols + (col - 1)


# Transition Model class definition
class TransitionModel:

    def __init__(self, states, actions, walls, terminalStates, probabilities, rows, cols):
        self.states = states
        self.actions = actions
        self.rows = rows
        self.cols = cols
        self.walls = walls
        self.terminalStates = terminalStates
        self.pForward = probabilities['pForward']
        self.pLeft = probabilities['pLeft']
        self.pRight = probabilities['pRight']
        self.pBackward = probabilities['pBackward']
        self.filteredStates = self.filterCorrectStates()

    # This method filters the states and neglects walls and terminals states
    def filterCorrectStates(self):
        filteredStates = []
        for state in self.states:
            if(not(self.isWall(state)) and not(self.isTerminalState(state))):
                filteredStates.append(state)
        return filteredStates

    # This method returns the list of next states when any particular action is performed
    def nextState(self, state, action):
        nextStates = []
        actionIndex = self.actions.index(action)
        forwardAction = action
        if(actionIndex == 0):
            leftAction = self.actions[len(self.actions) - 1]
            rightAction = self.actions[actionIndex + 1]
        elif(actionIndex == len(self.actions) - 1):
            leftAction = self.actions[actionIndex - 1]
            rightAction = self.actions[0]
        else:
            leftAction = self.actions[actionIndex - 1]
            rightAction = self.actions[actionIndex + 1]
        
        nextStates.append({
            'state': self.newState(state, forwardAction),
            'probability': self.pForward
            });
        nextStates.append({
            'state': self.newState(state, leftAction),
            'probability': self.pLeft
            });
        nextStates.append({
            'state': self.newState(state, rightAction),
            'probability': self.pRight
            });
        return nextStates
    
    # This method returns the exact new state on performing a particular action
    def newState(self, state, action):
        [row, col] = state
        stateIndex = getStateIndex(state, self.cols)
        newState = []
        if(action == 'N'):
            if(col == self.cols or self.isWall(self.states[stateIndex + 1])):
                newState = [state[0], state[1]]
            else:
                newState = [self.states[stateIndex + 1][0], self.states[stateIndex + 1][1]]
        elif(action == 'S'):
            if(col == 1 or self.isWall(self.states[stateIndex - 1])):
                newState = [state[0], state[1]]
            else:
                newState = [self.states[stateIndex - 1][0], self.states[stateIndex - 1][1]]
        elif(action == 'E'):
            if(row == self.rows or self.isWall(self.states[stateIndex + self.cols])):
                newState = [state[0], state[1]]
            else:
                newState = [self.states[stateIndex + self.cols][0], self.states[stateIndex + self.cols][1]]
        elif(action == 'W'):
            if(row == 1 or self.isWall(self.states[stateIndex - self.cols])):
                newState = [state[0], state[1]]
            else:
                newState = [self.states[stateIndex - self.cols][0], self.states[stateIndex - self.cols][1]]
        else:
            newState = [state[0], state[1]]
        
        return newState
    
    # This method return Boolean - whether the state is a wall or not
    def isWall(self, state):
        isNextStateWall = False
        for wall in self.walls:
            if(wall[0] == state[0] and wall[1] == state[1]):
                isNextStateWall = True
                break
        return isNextStateWall

    # This method return Boolean - whether the state is a terminal state or not
    def isTerminalState(self, state):
        isTerminalState = False
        for tState in self.terminalStates:
            if(tState['state'][0] == state[0] and tState['state'][1] == state[1]):
                isTerminalState = True
                break
        return isTerminalState


# Class definition for Reward
class Reward:
    states = []
    rewards = {}

    # class method to set initial Rewards for states
    @classmethod
    def setStateRewards(cls, states, terminalStates, reward):
        cls.states = states
        for state in cls.states:
            cls.rewards[''.join(str(el) for el in state)] = reward
        for tState in terminalStates:
            cls.rewards[''.join(str(el) for el in tState['state'])] = tState['reward']
    
    # a class method to get reward - Reward function
    @classmethod
    def getReward(cls, state):
        return cls.rewards[''.join(str(el) for el in state)]


# Class definition of Utility function
class Utility: 

    # initialize a utility function
    def __init__(self, states, values):
        self.states = states
        self.values = values   

    # get value of utility for a particular state - equivalent of U(s)
    def getUtilityForState(self, state, stateIndex):
        return self.values[stateIndex]

    # set value of utility for a particular state
    def setUtilityForState(self, state, stateIndex, value):
        self.values[stateIndex] = value

    # returns the utilties of all states
    def getAllUtilities(self):
        return self.values


# This method performs the Value Iteration step
def valueIteration(mdp, e, df):
    convergingUtility = {}

    # set initial values to be 0 for each state
    values = [0 for s in mdp.states]
    utility = Utility(mdp.states, values)

    while(True):
        maxChange = 0
        values = [value for value in utility.getAllUtilities()]
        convergingUtility = Utility(mdp.states, values)

        printMDP(mdp.tModel.rows, mdp.tModel.cols, utility.getAllUtilities())
        print('\n')
        
        # iterate over each state
        for state in mdp.tModel.filteredStates:
            newValues = []

            # perform every possible action
            for action in mdp.actions:
                newValues.append(QValue(mdp, state, action, convergingUtility, df))

            # find max value
            maxNewValue = max(newValues)

            stateIndex = getStateIndex(state, mdp.tModel.cols)

            # update the utility
            utility.setUtilityForState(state, stateIndex, maxNewValue)
            
            # set max change
            if (abs(utility.getUtilityForState(state, stateIndex) - convergingUtility.getUtilityForState(state, stateIndex)) > maxChange):
                maxChange = abs(utility.getUtilityForState(state, stateIndex) - convergingUtility.getUtilityForState(state, stateIndex))
        
        # break condition
        if(maxChange < ((e * (1 - df))/df) ):
            break

    # returns converged utility
    return convergingUtility


# This method returns the QValue w.r.t action - equivalent of Q(mdp, S, a , U)
def QValue(mdp, state, action, utility, df):
    totalUtilityValue = 0
    for newState in mdp.tModel.nextState(state, action):
        totalUtilityValue += newState['probability'] * ( mdp.rewardFunc(newState['state']) + ( df * utility.getUtilityForState(newState['state'], getStateIndex(newState['state'], mdp.tModel.cols)) ))
    return totalUtilityValue


# This method returns the QValue given a policy - equivalent of Q(mdp, S, pi , U)
def QValuePi(mdp, state, policy, utility, df):
    totalUtilityValue = 0
    stateIndex = getStateIndex(state, mdp.tModel.cols)
    action = policy.getPolicyForState(state, stateIndex)
    for newState in mdp.tModel.nextState(state, action):
        totalUtilityValue += newState['probability'] * ( mdp.rewardFunc(newState['state']) + ( df * utility.getUtilityForState(newState['state'], getStateIndex(newState['state'], mdp.tModel.cols)) ))
    return totalUtilityValue


# Class definition of Policy Function
class Policy:

    # constructor for policy function
    def __init__(self, policyList, states):
        self.policyList = policyList
        self.states = states

    # set/update value of policy for a particular state
    def setPolicyForState(self, state, stateIndex, action):
        self.policyList[stateIndex] = action

    # get value of policy for a particular state - equivalent of pi(s)
    def getPolicyForState(self, state, stateIndex):
        return self.policyList[stateIndex]

    # get policy for all states
    def getAllPolicy(self):
        return self.policyList


# This method returns the best action (which returns the highest utility of all actions) if the given policy is executed
def calculatePolicy(state, actions, tModel, utility, rewardFunc, df):
    policyValues = []
    for action in actions:
        totalPolicyValue = 0
        for nextState in tModel.nextState(state, action):
            totalPolicyValue += nextState['probability'] * ( rewardFunc(nextState['state']) + (df * utility.getUtilityForState(nextState['state'], getStateIndex(nextState['state'], tModel.cols)) ))
        policyValues.append(totalPolicyValue)
    maxValue = max(policyValues)
    
    maxValueIndex = policyValues.index(maxValue)

    return actions[maxValueIndex]

# This method performs the policy evaluation for Modified Policy Iteration Algorithm and returns an utility
def policyEvaluation(policy, utility, mdp, df, k):
    # Modified Policy Iteration because instead of evaluating Policy once, it is iterated for k times with Bellman update
    for i in range(k):
        for state in mdp.tModel.filteredStates:
            stateIndex = getStateIndex(state, mdp.tModel.cols)
            utility.setUtilityForState(state, stateIndex, QValuePi(mdp, state, policy, utility, df))
    return utility


# This method performs policy Iteration on an MDP given the mdp and discount factor
def policyIteration(mdp, df):
    initialPolicyList = setInitialPolicyValues(mdp.tModel)
    for i in range(0, len(initialPolicyList)):
        initialPolicyList[i] = mdp.actions[random.randrange(0, len(mdp.actions))] if(initialPolicyList[i] == '') else initialPolicyList[i]

    # create a policy with random actions
    policy = Policy(initialPolicyList, mdp.states)

    # initial utility values
    values = [0 for s in mdp.states]
    utility = Utility(mdp.states, values)

    # number of value iteration steps to do Bellman Update
    k = 20

    while(True):
        utility = policyEvaluation(policy, utility, mdp, df, k)
        unchanged = True

        for state in mdp.tModel.filteredStates:
            action = calculatePolicy(state, mdp.actions, mdp.tModel, utility, Reward.getReward, df)

            stateIndex = getStateIndex(state, mdp.tModel.cols)
            if(action != policy.getPolicyForState(state, stateIndex)):
                policy.setPolicyForState(state, stateIndex, action)
                unchanged = False
        if(unchanged):
            return policy


# This method sets the initial Policy for Policy Iteration
def setInitialPolicyValues(tModel):
    initialPolicy = []
    for state in tModel.states:
        if(tModel.isWall(state)):
            initialPolicy.append('-')
        elif(tModel.isTerminalState(state)):
            initialPolicy.append('T')
        else:
            initialPolicy.append('')

    return initialPolicy


# This method prints the MDP grid
def printMDP(rows, cols, itemsToPrint):
    for i in range(0, cols):
        counter = cols - i - 1
        toPrint = ''
        while(counter < cols * rows):
            toPrint += str(itemsToPrint[counter])
            toPrint += '    '
            counter += cols
        print(toPrint)
        print('\n')


# This method parses the input file into MDP data
def parseInputFile(fName):
    rows = 0
    cols = 0
    terminalStates = []
    walls = []
    nonTerminalReward = 0
    tProbabilities = {
        'pForward': 0,
        'pLeft': 0,
        'pRight': 0,
        'pBackward': 0
    }

    df = 0
    epsilon = 0

    # read the file
    with open(fName,'r') as f:
        line = f.readlines()
        rows = int("".join(line[2].split()).split(":")[1][0])
        cols = int("".join(line[2].split()).split(":")[1][1])

        wallItems = "".join(line[6].split()).split(":")[1].split(",")
        for item in wallItems:
            walls.append([int(item[0]), int(item[1])])

        terminalItems = "".join(line[10].split()).split(":")[1].split(",")
        for item in terminalItems:
            terminalStates.append({
                'state': [int(item[0]), int(item[1])],
                'reward': 0 + float(item[2] + item[3])
            })

        nonTerminalReward = float("".join(line[14].split()).split(":")[1])
        
        filteredProbs = []
        for item in " ".join(line[18].split()).split(":")[1].split(" "):
            if(item != ""):
                filteredProbs.append(item)
        tProbabilities['pForward'] = float(filteredProbs[0])
        tProbabilities['pLeft'] = float(filteredProbs[1])
        tProbabilities['pRight'] = float(filteredProbs[2])
        tProbabilities['pBackward'] = float(filteredProbs[3])
        
        df = float("".join(line[20].split()).split(":")[1])

        epsilon = float("".join(line[22].split()).split(":")[1])

    # returns parsed MDP Data
    return {
        'rows': rows,
        'cols': cols,
        'terminalStates': terminalStates,
        'walls': walls,
        'nonTerminalReward': nonTerminalReward,
        'tProbabilities': tProbabilities,
        'df': df,
        'epsilon': epsilon
    }
        

# This method is called on program execution and it solves the specified Grid MDP Problem
def solveMDPProblem():
    # get parsed data from input file
    parsedData = parseInputFile("mdp_input.txt")

    rows = parsedData['rows']
    cols = parsedData['cols']

    actions = ['N', 'E', 'S', 'W']

    states = buildStates(rows, cols)

    walls = parsedData['walls']
    reward = parsedData['nonTerminalReward']
    terminalStates = parsedData['terminalStates']
    discountFactor = parsedData['df']
    epsilon = parsedData['epsilon']
    tProbabilities = parsedData['tProbabilities']

    Reward.setStateRewards(states, terminalStates, reward)

    tModel = TransitionModel(states, actions, walls, terminalStates, tProbabilities, rows, cols)

    mdp = MDP(states, actions, tModel, Reward.getReward)

    # Utility after convergence (Value Iteration)
    utility = valueIteration(mdp, epsilon, discountFactor)

    initialPolicy = setInitialPolicyValues(tModel)
    
    policy = Policy(initialPolicy, states)
    for state in tModel.filteredStates:
        stateIndex = getStateIndex(state, tModel.cols)
        policy.setPolicyForState(state, stateIndex, calculatePolicy(state, actions, tModel, utility, Reward.getReward, discountFactor))

    # print the values with value iteration
    print('\n')
    print("########################### Utility Vector with Value Iteration is: \n")
    printMDP(rows, cols, utility.getAllUtilities())

    # print the policy with value iteration
    print("########################### Policy Vector with Value Iteration is: \n")
    printMDP(rows, cols, policy.getAllPolicy())

    policyWithPI = policyIteration(mdp, discountFactor)

    # print the policy after modified policy iteration
    print("########################### Policy Vector after Modified Policy Iteration is: \n")
    printMDP(rows, cols, policyWithPI.getAllPolicy())


# Execute the solveMDPproblem method
solveMDPProblem()



