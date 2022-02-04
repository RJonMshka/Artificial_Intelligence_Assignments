import sys
import numpy as np
import json


# This method returns attribute value of output which is max in number
def PluralityValue(output):
    value, count = np.unique(output, return_counts=True)
    maxCount = np.argmax(count)
    return value[maxCount]

# if all outputs are the same
def isClassificationSame(output):
    uniqueOutput = np.unique(output)
    isSame = False
    if(len(uniqueOutput) == 1):
        isSame = True
    return isSame


# This method calculates entropy
def CalculateEntropy(data):
    entropy = 0
    newData, countValue = np.unique(data, return_counts=True)
    probabilities = countValue/len(data)
    for prob in probabilities:
        if(prob != 0.0 or prob != 0):
            entropy += ( -1 * prob * np.log2(prob))
    return entropy


# This method is used to filter the output
def filteredOutput(y, x, val):
    result = []
    for index in range(0, len(x)):
        if(x[index] == val):
            result.append(y[index])

    return result


# This method calulates the information gain w.r.t to output for set of examples
def InformationGain(output, exampleAttr):
    result = CalculateEntropy(output)
    exampleData, countValue = np.unique(exampleAttr, return_counts=True)
    probabilities = countValue/len(exampleAttr)

    for i in range(0, len(exampleData)):
        result += (-1 * probabilities[i] * CalculateEntropy(filteredOutput(output, exampleAttr, exampleData[i])))
    
    return result


# create partition and returns attribute specific array index and attribute value
def getAttributeSetList(attrSpecificArray):
    uniqueAttrValues = np.unique(attrSpecificArray)
    result = []
    for value in uniqueAttrValues:
        result.append({
            "attrValue": value,
            "indexes": (attrSpecificArray == value).nonzero()[0]
        })
    
    return result


# Main logic for Decision tree learning
def LearnDecisionTree(examples, attrs, output, parentOutput):
    if(len(examples) == 0):
        return PluralityValue(parentOutput)
    elif(isClassificationSame(output)):
        return output[0]
    elif(len(attrs) == 0):
        return PluralityValue(output)
    else:
        examplesArray = np.array(examples)
        gainArray = np.array([round(InformationGain(output, exampleAttr), 2) for exampleAttr in examplesArray.T])
        maxArray = np.argwhere(gainArray == np.amax(gainArray))
        attrIndex = maxArray[0][0]
        setList = getAttributeSetList(examplesArray[:, attrIndex])

        tree = {}

        for attrValue in setList:
            newOutput = np.array(output).take(attrValue["indexes"], axis=0).tolist()
            newExamplesArray = examplesArray.take(attrValue["indexes"], axis=0)
            newExamplesArray = np.delete(newExamplesArray, attrIndex, 1)
            newExamplesList = newExamplesArray.tolist()
            newAttrs = attrs[:attrIndex] + attrs[attrIndex+1 : ]
            keyName = attrs[attrIndex] + "-----" + attrValue["attrValue"] + "----->"
            tree[keyName] = LearnDecisionTree(newExamplesList, newAttrs, newOutput, output)
        
        return tree;



# read the file
fileName = sys.argv[1]

fileData = []

# open file
with open(fileName, 'r') as f:
    for line in f:
        words = line.split(',')
        fileData.append([item.strip() for item in words])

# given attributes
attributes = ["Alternate", "Bar", "Fri/Sat", "Hungry", "Patrons", "Price", "Raining", "Reservation", "Type", "Wait Estimate"]

# output - y : which needs to be estimated
output = [row[-1] for row in fileData]

# sample training data
examples = [row[0:-1] for row in fileData]

# decision tree
decisionTree = LearnDecisionTree(examples, attributes, output, output)
print("<<<<<<<... Decision Tree .......>>>>>>>>>>")
print(json.dumps(decisionTree, sort_keys=True, indent=4))
p = 0
n = 0
# Alpha for deviation of pattern from null hypothesis (used for pruning using Chi-squared test)
alpha = 0.05

# populate p and n
val, count = np.unique(output, return_counts=True)
for index in range(0, len(val)):
    if(val[index] == "Yes"):
        p = count[index]
    elif(val[index] == "No"):
        n = count[index]

dataValues = {}

# This method calculates p,n for each node and its branches
def pruneTree(tree, parent):
    if(isinstance(tree, dict)):
        for item in tree:
            # not a leaf node
            attrName = item.split("-----")[0]
            branchName = item.split("-----")[1]
            attrIndex = attributes.index(attrName)

            if(item not in dataValues):
                dataValues[item] = {}
                dataValues[item] = {}
                dataValues[item]["p"] = 0
                dataValues[item]["n"] = 0
                dataValues[item]["pr"] = 0
                dataValues[item]["nr"] = 0
            
            branchIndices = (np.array(examples)[:, attrIndex] == branchName).nonzero()[0]
            val1, count1 = np.unique(np.array(output).take(branchIndices, axis=0), return_counts=True)
            for i in range(0, len(val1)):
                if(val1[i] == "Yes"):
                    dataValues[item]["p"] = count[i]
                else:
                    dataValues[item]["n"] = count[i]
            dataValues[item]["pr"] = p * (dataValues[item]["p"] + dataValues[item]["n"]) / (p + n)
            dataValues[item]["nr"] = n * (dataValues[item]["p"] + dataValues[item]["n"]) / (p + n)

            pruneTree(tree[item], tree)
    elif(isinstance(tree, str)):
        # leaf node
        areAllChildrenLeaf = True
        for item in parent:
            if(isinstance(parent[item], dict)):
                areAllChildrenLeaf = False
                for newItem in parent[item]:
                    # Iot a leaf node
                    attrName = newItem.split("-----")[0]
                    branchName = newItem.split("-----")[1]
                    attrIndex = attributes.index(attrName)

                    if(not(newItem in dataValues)):
                        dataValues[newItem] = {}
                    dataValues[newItem]["p"] = 0
                    dataValues[newItem]["n"] = 0
                    dataValues[newItem]["pr"] = 0
                    dataValues[newItem]["nr"] = 0
                    branchIndices = (np.array(examples)[:, attrIndex] == branchName).nonzero()[0]
                    val1, count1 = np.unique(np.array(output).take(branchIndices, axis=0), return_counts=True)
                    for i in range(0, len(val1)):
                        if(val1[i] == "Yes"):
                            dataValues[newItem]["p"] = count1[i]
                        elif(val[i] == "No"):
                            dataValues[newItem]["n"] = count1[i]
                    dataValues[newItem]["pr"] = p * (dataValues[newItem]["p"] + dataValues[newItem]["n"]) / (p + n)
                    dataValues[newItem]["nr"] = n * (dataValues[newItem]["p"] + dataValues[newItem]["n"]) / (p + n)

                    pruneTree(parent[item][newItem], parent[item])


pruneTree(decisionTree, None)
for item in decisionTree:
    deviation = 0
    positives = 0
    negatives = 0
    # chi-square test
    deviation += ( ( (dataValues[item]["p"] - dataValues[item]["pr"]) * (dataValues[item]["p"] - dataValues[item]["pr"]) / dataValues[item]["pr"] ) + ( (dataValues[item]["n"] - dataValues[item]["nr"]) * (dataValues[item]["n"] - dataValues[item]["nr"]) / dataValues[item]["nr"] ) )
    positives += dataValues[item]["p"]
    negatives += dataValues[item]["n"]
    if(deviation < alpha):
        pruneItem = True

    if(pruneItem):
        if(positives < negatives):
            decisionTree[item] = "Yes"
        else:
            decisionTree[item] = "No"

print("\n")
print("<<<<<<<<<<<<<<< Decision tree after pruning >>>>>>>>>>>")
print(decisionTree)





