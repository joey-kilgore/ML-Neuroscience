import math 
from random import *
import copy

mutationList = []   # The global list of connections

class Connection:  
    # The connection stores information for how two nodes are connected
    def __init__(self, startNode, endNode, w, enabled):
        self.start = startNode  
        self.end = endNode
        self.weight = w
        self.enabled = enabled

class Node:
    # Nodes store their connections and their value as its calculated
    def __init__(self, index):
        self.connections = []
        self.index = index
        self.value = 0
        self.numInputs = 0
        self.calcedInputs = 0
    
    def addConection(self, connection):
        self.connections.append(connection)

def calcNetwork(genome, inputs):
    outputs = {}    # Store the outputs from the network in this dictionary
    nodes = makeNodeList(genome)    # Make the node list based off the genome (the list of connections)

    # The process of calculating the network requires using a queue to tell which nodes have been calculated
    #   when a node has gotten all of its inputs, it is added to the queue
    #   when there are no more items in the queue then the network has been calculated
    nodeQueue = setInputNodes(nodes, inputs)    # The input nodes are set, and the process of calculating the outputs 
    while len(nodeQueue) > 0:   # Loop until all nodes have been processed
        curNode = nodeQueue[0]   # Dequeue the next node
        nodeQueue = nodeQueue[1:]
        if len(curNode.connections) == 0:   # If a node has no connections then it must be an output node
            outputs[curNode.index] = curNode.value    #   and its value is added to the outputs dictionary
        
        else:   # If there is at least one connection, then each connection is processed
            for con in curNode.connections:
                nodes[con.end].value += con.weight * curNode.value  # The weight * value is added to the next nodes value
                nodes[con.end].calcedInputs+=1  # The number of calculated inputs is incrememted
                if nodes[con.end].numInputs == nodes[con.end].calcedInputs : # All inputs have been calculated and the node can be activated
                    nodes[con.end].value = activationFunction(nodes[con.end].value)
                    nodeQueue.append(nodes[con.end])    # After activating the node, it can be appended to the queue to be processed
    
    return outputs # The final outputs are returned

def activationFunction(num):
    return 1 / (1 + math.exp(-num))

def makeNodeList(genome):
    nodeList = {}
    # All the connections within the genome are checked for new nodes
    for con in genome:
        if con.enabled == True: # Some connections are disable later on (through making new nodes)
            if not con.start in nodeList:   # if the starting node has not been observed before a new node is made
                nodeList[con.start] = Node(con.start)
            nodeList[con.start].addConection(con)   # all starting nodes must store the connection (needed for calcNetwork)
            if not con.end in nodeList:     # if the ending node has not been observed before a new node is made
                nodeList[con.end] = Node(con.end)
            nodeList[con.end].numInputs += 1    # all ending nodes must keep track of how many inputs they have (needed for calcNetwork)
    return nodeList 

def setInputNodes(nodes, inputs):
    index = 0
    inputNodes = []
    # Setting the inputs takes advantage of knowing that the first nodes of the list must be the input nodes
    # This is known based on the fact the initial nodes are indexed as the first nodes, and then the output, and
    #   then all hidden nodes are created and have higher indexes because they are created later on after mutations
    for value in inputs:
        nodes[index].value = value  # Set the value of the input node
        if nodes[index].numInputs > 0:  # Ensure that the node is actually an input
            print("ERROR INPUT CONNECTIONS ON INPUT NODE")
        inputNodes.append(nodes[index])
        index += 1
    return inputNodes

def initGenome(numInputs, numOutputs):
    global mutationList
    for inputIndex in range(numInputs):
        for outputIndex in range(numOutputs):
            mutationList.append(Connection(inputIndex, outputIndex+numInputs, random()*2-1, 1))
    return copy.deepcopy(mutationList)

def printGenome(genome):
    for con in genome:
        print(str(con.start) + "->" + str(con.end) + "  " + ("ENABLED" if con.enabled == 1 else "DISABLED"))