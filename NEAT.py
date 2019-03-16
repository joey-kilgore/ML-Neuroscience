import math 
from random import *
import copy

# NEAT or NeuroEvolutionary Augmented Topologies is a ML algorithm and is described best at the link below:
# https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume21/stanley04a-html/node3.html

mutationDictionary = {}   # The global list of connections
nodeCount = 0
geneCount = 0

class Connection:  
    # The connection stores information for how two nodes are connected
    def __init__(self, genomeIndex, startNode, endNode, w, enabled, isInput, isOutput):
        self.index = genomeIndex
        self.start = startNode  
        self.end = endNode
        self.weight = w
        self.enabled = enabled
        self.isInput = isInput
        self.isOutput = isOutput

class Node:
    # Nodes store their connections and their value as its calculated
    def __init__(self, index, isInput, isOutput):
        self.connections = []
        self.index = index
        self.value = 0
        self.numInputs = 0
        self.calcedInputs = 0
        self.isInput = isInput
        self.isOutput = isOutput
    
    def addConection(self, connection):
        self.connections.append(connection)

class Genome:
    # Genome stores the genes and nodes that define a network
    def __init__(self):
        self.connections = []
        self.nodes = {}
        self.inputNodes = []
        self.outputNodes = []

def calcNetwork(genome, inputs):
    # The process of calculating the network requires using a queue to tell which nodes have been calculated
    #   when a node has gotten all of its inputs, it is added to the queue
    #   when there are no more items in the queue then the network has been calculated
    setInputNodes(genome, inputs)    # The input nodes are set, and the process of calculating the outputs 
    nodeQueue = genome.inputNodes
    while len(nodeQueue) > 0:   # Loop until all nodes have been processed
        curNode = nodeQueue[0]   # Dequeue the next node
        nodeQueue = nodeQueue[1:]
        for con in curNode.connections:
            genome.nodes[con.end].value += con.weight * curNode.value  # The weight * value is added to the next nodes value
            genome.nodes[con.end].calcedInputs+=1  # The number of calculated inputs is incrememted
            if genome.nodes[con.end].numInputs == genome.nodes[con.end].calcedInputs : # All inputs have been calculated and the node can be activated
                genome.nodes[con.end].value = activationFunction(genome.nodes[con.end].value)
                nodeQueue.append(genome.nodes[con.end])    # After activating the node, it can be appended to the queue to be processed
    
    outputs = []
    for node in genome.outputNodes: # The final outputs are returned
        outputs.append(node.value)
    return outputs


def activationFunction(num):
    return 1 / (1 + math.exp(-num))

def makeNodeList(genome):
    nodeList = {}
    # All the connections within the genome are checked for new nodes
    for con in genome:
        if con.enabled == True: # Some connections are disable later on (through making new nodes)
            if not con.start in nodeList:   # if the starting node has not been observed before a new node is made
                nodeList[con.start] = Node(con.start, con.isInput, 0)
            nodeList[con.start].addConection(con)   # all starting nodes must store the connection (needed for calcNetwork)
            if not con.end in nodeList:     # if the ending node has not been observed before a new node is made
                nodeList[con.end] = Node(con.end, 0, con.isOutput)
            nodeList[con.end].numInputs += 1    # all ending nodes must keep track of how many inputs they have (needed for calcNetwork)
    return nodeList 

def setInputNodes(genome, inputs):
    for i in range(len(inputs)):
        genome.inputNodes[i].value = inputs[i]

def initGenome(numInputs, numOutputs):
    # initGenome is meant to be used for creating genomes with no parents, ie the initial genomes
    global mutationDictionary   # the mutationDictionary is needed for a global collection of all genomes
    global nodeCount            # nodeCount keeps track of how many nodes have been created across all genomes
    global geneCount            # genomeCount keeps track of hamny new genes have been created
    initGenome = Genome()   # initGene stores the new genome being created
    inputNodes = []
    # The simplest (ie original) genome is simply having all input nodes have a single direct connection to all output nodes
    for inputIndex in range(numInputs):             # Loop through every input node
        nodeConnections = []
        for outputIndex in range(numOutputs):       # Loop through every output node
            # Create the connection between input and output node with the following parameters
            # connection index = current geneCount, and is needed for looking up the gene in the global mutationDictionary
            # starting node = the input index which goes from 0 to len(numInputs)-1
            # ending node = the outputIndex+numInputs which goes from len(numInputs) to len(numInputs)+len(numOutputs)-1 
            # weight = random number from -1 to 1
            # enabled = 1 (ie the connection is enabled)
            con = Connection(geneCount, inputIndex, outputIndex+numInputs, random()*2-1, 1, 1, 1) 
            mutationDictionary[geneCount] = copy.copy(con)     # a copy is saved to the global list
            initGenome.connections.append(con)      # a reference is appended to the initial genome being created
            nodeConnections.append(con)             # the same reference is saved for making the list of connections for the node
            geneCount+=1    # a new gene was created so the geneCount is incremented
        newNode = Node(nodeCount, 1, 0) # generate a new input node
        newNode.connections = nodeConnections   # set the connections for this input node to all the new connections made for this node
        initGenome.nodes[nodeCount] = newNode # save the new node
        inputNodes.append(newNode)
        nodeCount += 1
    initGenome.inputNodes = inputNodes

    # now all connections have been made and the input nodes, but we still need to make the output nodes
    outputNodes = []
    for outputIndex in range(numOutputs):
        newNode = Node(nodeCount, 0, 1) # create a new node, and set it as an output node
        initGenome.nodes[nodeCount] = newNode    # save the node to the node list
        outputNodes.append(newNode)         #   and to the list of output nodes
        nodeCount += 1  # a new node was created so the global index tracker is incremented
    initGenome.outputNodes = outputNodes

    return initGenome

def printGenome(genome):
    # printGenome gives a way of looking at all the genes of a genome
    for con in genome.connections:
        print(str(con.index) + "\t" + str(con.start) + "->" + str(con.end) + "\t" + (str(con.weight) if con.enabled == 1 else "DISABLED\t") + "\t" + ("INPUT" if con.isInput==1 else "HIDDEN") + "\t" + ("OUTPUT" if con.isOutput==1 else "HIDDEN"))

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
    
    randomGene = genome.connections[randint(0,len(genome.connections)-1)]   # a random gene is chosen
    while randomGene.enabled != 1:                  # the gene must be enabled (because you cant disable a connection thats already disabled)
        randomGene = genome.connections[randint(0,len(genome.connections)-1)]   # keep picking a gene until an enabled one is found
    randomGene.enabled = 0  # disable the original connection
    
    newConnect1 = Connection(geneCount, randomGene.start, nodeCount, random()*2-1, 1, randomGene.isInput, 0) # build the first new connection TO the new node
    newConnect2 = Connection(geneCount+1, nodeCount, randomGene.end, random()*2-1, 1, 0, randomGene.isOutput) # build the second new connection FROM the new node
    newNode = Node(nodeCount,0,0)           # build the new hidden node
    newNode.connections.append(newConnect2) # add its connection out
    newNode.numInputs = 1                   # add its one connection in
    
    genome.connections.append(newConnect1)  # add the new genes to the genome
    genome.connections.append(newConnect2)
    genome.nodes[nodeCount] = newNode   
    
    mutationDictionary[geneCount] = copy.copy(newConnect1)  # save a copy of the new genes to the global list
    mutationDictionary[geneCount+1] = copy.copy(newConnect2)

    nodeCount += 1  # a new node is being created
    geneCount += 2  # two genes were created

    genome.nodes[randomGene.start].connections.remove(randomGene)   # now the original connection must be removed from the node
    genome.nodes[randomGene.start].connections.append(newConnect1)  # and the new connection is added

def addConnectionMutation(genome):
    # Creating a new connection is actually a nontrivial process
    # The connection must go from a node that already has a connection coming out (ie not an output node)
    # The connection must go to a node that already has an input connection (ie not an input node)
    # The connection cannot go to a node that is connected back to the original node (ie no loops)
    # No duplicate connections
    global mutationDictionary   # the mutationDictionary is needed for a global collection of all genomes
    global nodeCount            # nodeCount keeps track of how many nodes have been created across all genomes
    global geneCount            # genomeCount keeps track of hamny new genes have been created

    foundConnection = False
    while foundConnection == False:
        startNode = genome.connections[randint(0,len(genome.connections)-1)].start  # This means the start node already has at least one outgoing conenction
        endNode = genome.connections[randint(0,len(genome.connections)-1)].end      # This means the end node already has at least one input conneciton
        if startNode != endNode: # no loops
            foundConnection = True  # begine checking through all other genes in genome
            for gene in genome.connections:
                # check if any of the current genes are either the connection is already present or would create a loop
                if (gene.start == startNode and gene.end == endNode) or (gene.end == startNode and gene.start == endNode):
                    foundConnection = False
                    break
    
    newCon = Connection(geneCount, startNode, endNode, random()*2-1, 1, genome.nodes[startNode].isInput, genome.nodes[endNode].isOutput) # Create the new connection
    mutationDictionary[geneCount] = copy.copy(newCon)  # Save copy of gene in global list of all genes
    genome.connections.append(newCon)    # Add a gene to genomes list of connections