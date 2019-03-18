import math 
import random
import copy

# NEAT or NeuroEvolutionary Augmented Topologies is a ML algorithm and is described best at the link below:
# https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume21/stanley04a-html/node3.html

mutationDictionary = {}   # The global list of connections
nodeCount = 0   # global tracker for indexing new nodes
geneCount = 0   # global tracker for indexing new genes

class Connection:  
    # The connection stores information for how two nodes are connected
    def __init__(self, genomeIndex, startNode, endNode, w, enabled, isInput, isOutput):
        self.index = genomeIndex    # this is the key in genome.connections and the mutationDictionary
        self.start = startNode      # the index of the starting node of this connection
        self.end = endNode          # the index of the ending node of this connection
        self.weight = w             # the weight of the connection
        self.enabled = enabled      # whether this connection is enabled (or disabled)
        self.isInput = isInput      # whether the starting node is an input node
        self.isOutput = isOutput    # whether the ending node is an output node

class Node:
    # Nodes store their connections and their value as its calculated
    def __init__(self, index, isInput, isOutput):
        self.connections = []       # the list of connections (used when calculating the network)
        self.index = index          # this is the key in genome.nodes
        self.value = 0              # this stores the value of the node during calculation
        self.numInputs = 0          # keeps track of the total number of inputs the node has
        self.calcedInputs = 0       # keeps track of how many inputs have been calculated (used when calculating the network)
        self.isInput = isInput      # is the node an input node
        self.isOutput = isOutput    # is the node an output node

class Genome:
    # Genome stores the genes and nodes that define a network
    def __init__(self):
        self.connections = {}   # dictionary for all genes (key = connection index, value = gene)
        self.nodes = {}         # dictionary for all nodes (key = node index, value = node)
        self.inputNodes = []    # list of input nodes
        self.outputNodes = []   # list of output nodes

def calcNetwork(genome, inputs):
    # The process of calculating the network requires using a queue to tell which nodes have been calculated
    #   when a node has gotten all of its inputs, it is added to the queue
    #   when there are no more nodes in the queue then the network has been calculated

    for node in list(genome.nodes.values()):    # set the value of all nodes to 0
        node.value = 0

    setInputNodes(genome, inputs)    # The input nodes are set, and the process of calculating the outputs 
    nodeQueue = genome.inputNodes
    while len(nodeQueue) > 0:   # Loop until all nodes have been processed
        curNode = nodeQueue[0]   # Dequeue the next node
        nodeQueue = nodeQueue[1:]
        for con in curNode.connections:
            if con.enabled == 1:    # ensure the connections are enabled
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
            con = Connection(geneCount, inputIndex, outputIndex+numInputs, random.random()*2-1, 1, 1, 1) 
            mutationDictionary[geneCount] = copy.copy(con)     # a copy is saved to the global list
            initGenome.connections[geneCount] = con      # a reference is appended to the initial genome being created
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
    for con in genome.connections.values():
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
    
    randomGene = random.choice(list(genome.connections.values()))   # a random gene is chosen
    while randomGene.enabled != 1:                  # the gene must be enabled (because you cant disable a connection thats already disabled)
        randomGene = random.choice(list(genome.connections.values())) # keep picking a gene until an enabled one is found
    randomGene.enabled = 0  # disable the original connection
    
    # build the first new connection TO the new node
    newConnect1 = Connection(geneCount, randomGene.start, nodeCount, random.random()*2-1, 1, randomGene.isInput, 0) 
    # build the second new connection FROM the new node
    newConnect2 = Connection(geneCount+1, nodeCount, randomGene.end, random.random()*2-1, 1, 0, randomGene.isOutput) 
    newNode = Node(nodeCount,0,0)           # build the new hidden node
    newNode.connections.append(newConnect2) # add its connection out
    newNode.numInputs = 1                   # add its one connection in
    
    genome.connections[geneCount] = newConnect1  # add the new genes to the genome
    genome.connections[geneCount+1] = newConnect2
    genome.nodes[nodeCount] = newNode   # add the new node to the genome
    
    mutationDictionary[geneCount] = copy.copy(newConnect1)  # save a copy of the new genes to the global list
    mutationDictionary[geneCount+1] = copy.copy(newConnect2)

    nodeCount += 1  # a new node is being created
    geneCount += 2  # two genes were created

    randomGene.enabled = 0   # now the original connection must be disabled
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
        startNode = random.choice(list(genome.connections.values())).start  # This means the start node already has at least one outgoing conenction
        endNode = random.choice(list(genome.connections.values())).end      # This means the end node already has at least one input conneciton
        if startNode != endNode: # no loops
            foundConnection = True  # begine checking through all other genes in genome
            for gene in genome.connections.values():
                # check if any of the current genes are either the connection is already present or would create a loop
                if (gene.start == startNode and gene.end == endNode) or (gene.end == startNode and gene.start == endNode):
                    foundConnection = False
                    break
    
    # Create the new connection
    newCon = Connection(geneCount, startNode, endNode, random.random()*2-1, 1, genome.nodes[startNode].isInput, genome.nodes[endNode].isOutput)
    mutationDictionary[geneCount] = copy.copy(newCon)  # Save copy of gene in global list of all genes
    genome.connections[geneCount] = newCon    # Add a gene to genomes list of connections
    genome.nodes[newCon.start].connections.append(newCon)
    genome.nodes[newCon.end].numInputs += 1
    geneCount += 1  # a new gene was created

def mutateGenome(genome):
    newGenome = copy.deepcopy(genome)
    addNodeMutation(newGenome)
    return newGenome

def crossGenomes(parent1, parent2):
    global mutationDictionary   # the global dictionary of mutations is a key element in being able to cross genomes
    global geneCount    # the global gene count is also useful
    newGenome = Genome()
    for geneIndex in range(geneCount):  # loop through ALL known genes
        # check if the gene is in either parent, if not then the gene can be skipped
        if geneIndex in parent1.connections or geneIndex in parent2.connections:
            # if the gene is in only one parent then there is a 50% chance it will be skipped
            if not (geneIndex in parent1.connections and geneIndex in parent2.connections) and random.random() > 0.5:
                continue
            
            # the gene will be created
            newGene = copy.copy(mutationDictionary[geneIndex])
            
            # one parent is chosen at random and if the gene is disabled in that genome, then the child genome will also be disabled
            # if it is only in one parent than it it will be enabled
            # also if both parents have the gene disabled than this will disable the gene
            if random.random() > 0.5 and geneIndex in parent1.connections and parent1.connections[geneIndex].enabled == 0:
                newGenome.connections[geneIndex] = newGene
                newGene.enabled = 0
                continue
            elif geneIndex in parent2.connections and parent2.connections[geneIndex].enabled == 0:
                newGenome.connections[geneIndex] = newGene
                newGene.enabled = 0
                continue

            # at the this point the gene has been added and it is enabled
            addGeneToGenome(newGenome, newGene) # add the gene to the genome

    # the genome has a random selection of genes from the parents, but it may be missing input and output nodes
    # both parents should have the same number so it doesn't matter which parent we check against
    for node in parent1.inputNodes + parent1.outputNodes:
        if not node.index in newGenome.nodes:
            # find all possible valid connections from parents
            validGenes = []
            for gene in list(parent1.connections.values()) + list(parent2.connections.values()):
                if gene.enabled == 1 and gene.start == node.index:
                    validGenes.append(gene)
            chosenGene = random.choice(validGenes)  # pick a random valid gene
            addGeneToGenome(newGenome, chosenGene)  # add it to the genome

    # the genome has now been built but there are likely hidden or input nodes without connections out
    # and there are likely hidden and output nodes without any inputs
    isDone = False
    while not isDone:   # keep making fixes until the netork needs no additional modifications
        isDone = True
        for node in list(newGenome.nodes.values()):
            # check if the input or hidden nodes have at least one connection
            if node.isOutput != 1 and len(node.connections) == 0:
                # find all possible valid connections from parents
                validGenes = []
                for gene in list(parent1.connections.values()) + list(parent2.connections.values()):
                    if gene.enabled == 1 and gene.start == node.index:
                        validGenes.append(gene)
                chosenGene = random.choice(validGenes)  # pick a random valid gene
                addGeneToGenome(newGenome, chosenGene)  # add it to the genome
                isDone = False   # a modification was made
            
            # check if the output or hidden nodes have at least one input
            if node.isInput != 1 and node.numInputs == 0:
                # find all possible valid connections from parents
                validGenes = []
                for gene in list(parent1.connections.values()) + list(parent2.connections.values()):
                    if gene.enabled == 1 and gene.end == node.index:
                        validGenes.append(gene)
                chosenGene = random.choice(validGenes)  # pick a random valid gene
                addGeneToGenome(newGenome, chosenGene)  # add it to the genome
                isDone = False   # a modification was made
    
    # after the network is made and has been checked to elimate any unconnected nodes then the crossing is done
    return newGenome
    
def addGeneToGenome(genome, gene):
    # adding a gene to a genome requires more than simply adding it to the list of genes
    # we must also check if new nodes need to be added to the genome as well
    # the gene will be created
    newGene = copy.copy(mutationDictionary[gene.index])
    genome.connections[gene.index] = newGene    # the gene is added to the genome

    # check if the nodes for the gene does not exist in the genome already
    if not newGene.start in genome.nodes:
        # if the start node does not exist add it (and add it to the input node list if necesary)
        genome.nodes[newGene.start] = Node(newGene.start, newGene.isInput, 0)
        if newGene.isInput == 1:
            genome.inputNodes.append(genome.nodes[newGene.start])
    genome.nodes[newGene.start].connections.append(newGene) # add the connection to the start node

    if not newGene.end in genome.nodes:
        # if the end node does not exist add it (and add it to the output node list if necesary)
        genome.nodes[newGene.end] = Node(newGene.end, 0, newGene.isOutput)
        if newGene.isOutput == 1:
            genome.outputNodes.append(genome.nodes[newGene.end])
    genome.nodes[newGene.end].numInputs += 1    # add to the number of inputs to the end node

def canAddConnection(genome):
    # check if it is possible to add another connection to the network (some networks may be fully connected)
    numNodes = len(list(genome.nodes.values()))
    numInputs = len(genome.inputNodes)
    for node in list(genome.nodes.values()):
        # we need to check the input and hidden nodes to ensure they have no more connections
        if node.isOutput == 1:
            continue    # output nodes can be skipped because they have no outgoing connections
        elif node.isInput == 1:
            # input nodes must have a connection to every other node in the network if the network is full
            connectedNodes = []
            for con in node.connections:
                if not con.end in connectedNodes:
                    connectedNodes.append(con.end)
            # if there is less nodes connected to the input node than total non-input nodes, then there is at least one connection possible
            if len(connectedNodes) < (numNodes - numInputs):
                return True
        else:
            # now we must check hidden nodes
            # they must be connected to all output nodes to be a full network
            # they must also have or be connected to every other hidden node to be a full network
            connectedNodes = []
            # check and find all nodes connected to the node
            for con in node.connections:
                if not con.end in connectedNodes:
                    connectedNodes.append(con.end)
            # check that any hidden nodes not connected out of this node are connected into this node
            for checkNode in list(genome.nodes.values()):
                if (not checkNode.index in connectedNodes):
                    if checkNode.isOutput == 1:
                        # if the node that is not connected is an output then we found there is a possible connection
                        return True
                    elif checkNode.isInput != 1:
                        # check if the hidden node is connected in
                        for con in checkNode.connections:
                            if not con.end == node.index:
                                connectedNodes.append(con.end)

            # if there is less nodes connected to the input node than total non-input nodes, then there is at least one connection possible
            if len(connectedNodes) < (numNodes - numInputs):
                return True
    # all connections have been checked, and the network must be full
    return False