import math 
from random import *
import copy

mutationDictionary = {}   # The global list of connections
nodeCount = 0
geneCount = 0

class Connection:  
    # The connection stores information for how two nodes are connected
    def __init__(self, genomeIndex, startNode, endNode, w, enabled):
        self.index = genomeIndex
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
    # initGenome is meant to be used for creating genomes with no parents, ie the initial genomes
    global mutationDictionary   # the mutationDictionary is needed for a global collection of all genomes
    global nodeCount            # nodeCount keeps track of how many nodes have been created across all genomes
    global geneCount            # genomeCount keeps track of hamny new genes have been created
    initGenes = []   # initGene stores the new genome being created
    # The simplest (ie original) genome is simply having all input nodes have a single direct connection to all output nodes
    for inputIndex in range(numInputs):             # Loop through every input node
        for outputIndex in range(numOutputs):       # Loop through every output node
            # Create the connection between input and output node with the following parameters
            # connection index = current geneCount, and is needed for looking up the gene in the global mutationDictionary
            # starting node = the input index which goes from 0 to len(numInputs)-1
            # ending node = the outputIndex+numInputs which goes from len(numInputs) to len(numInputs)+len(numOutputs)-1 
            # weight = random number from -1 to 1
            # enabled = 1 (ie the connection is enabled)
            con = Connection(geneCount, inputIndex, outputIndex+numInputs, random()*2-1, 1) 
            mutationDictionary[geneCount] = con     # the node is added to the global list of genes
            initGenes.append(copy.copy(con))    # a copy is appended to the initial genome being created
            geneCount+=1    # a new gene was created so the geneCount is incremented

    nodeCount = numInputs+numOutputs # the number of new nodes created
    return initGenes    # return the new genome

def printGenome(genome):
    # printGenome gives a way of looking at all the genes of a genome
    for con in genome:
        print(str(con.index) + "\t" + str(con.start) + "->" + str(con.end) + "\t" + (str(con.weight) if con.enabled == 1 else "DISABLED"))

def addNodeMutation(genome):
    # addNodeMutation is one of the two mutations of the NEAT algorithm
    # a connection between two nodes is disabled, and in its place a new node is added that spans the connection
    # ie originally node 0 is connected to node 1
    #   that original connection is disabled
    #   now node 0 connects to node 2
    #   and node 2 connects to node 1
    global mutationDictionary   # the mutationDictionary is needed for a global collection of all genomes
    global nodeCount            # nodeCount keeps track of how many nodes have been created across all genomes
    global geneCount            # genomeCount keeps track of hamny new genes have been created
    
    randomGene = genome[randint(0,len(genome)-1)]   # a random gene is chosen
    while randomGene.enabled != 1:                  # the gene must be enabled (because you cant disable a connection thats already disabled)
        randomGene = genome[randint(0,len(genome)-1)]   # keep picking a gene until an enabled one is found
    randomGene.enabled = 0  # disable the original connection
    
    newConnect1 = Connection(geneCount, randomGene.start, nodeCount, random()*2-1, 1) # build the first new connection TO the new node
    newConnect2 = Connection(geneCount+1, nodeCount, randomGene.end, random()*2-1, 1) # build the second new connection FROM the new node
    nodeCount += 1  # a new node is being created
    
    genome.append(newConnect1)  # add the new genes to the genome
    genome.append(newConnect2)
    
    mutationDictionary[geneCount] = copy.copy(newConnect1)  # save a copy of the new genes to the global list
    mutationDictionary[geneCount+1] = copy.copy(newConnect2)
    geneCount += 2  # two genes were created