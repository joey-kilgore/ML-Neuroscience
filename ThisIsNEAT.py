import NEAT

# NeuroEvolutionary Augmented Topology or NEAT is extrememly useful for reinforcement learning
# For some background into the algorithm check out the following link
# https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume21/stanley04a-html/node3.html
# For some background on reinforcement learning check out this link
# https://en.wikipedia.org/wiki/Reinforcement_learning

# This code will give you a high level overview of what NEAT.py can do
# The first thing to know is that these networks that are generated are known as genomes
# Generating the initial genome is quite simple
#   You must specify the number of inputs the network will process, and how many outputs
genome1 = NEAT.initGenome(3,1)

# From this we can look at the genome using the printGenome() method
print("GENOME 1")
NEAT.printGenome(genome1)
# The output is shows all the genes in the genome. Given in the following format
# <gene index>  <start node> -> <end node>   <type of starting node>     <type of ending node>
# The initial genome will have just input and output nodes and they will be fully connected

# we can mutate this genome by adding a node (this is one of the two mutations outlined in the NEAT algorithm)
print("\nGENOME 1 AFTER NODE MUTATION")
NEAT.addNodeMutation(genome1)
NEAT.printGenome(genome1)

# the other type of mutation is a connection mutation, where a random connection is created between nodes
# Note that if the network is fully connected then we can't add any connections, so it's best practice to check
# you can check if a connection can be added by using the canAddConnection() method
print("\nCAN ANOTHER CONNECTION BE ADDED: " + str(NEAT.canAddConnection(genome1)))
NEAT.addConnectionMutation(genome1)
print("GENOME 1 AFTER CONNECTION MUTATION")
NEAT.printGenome(genome1)

# now that we have a network, we can give it input and it will give out output
print("\nCALCULATE OUPTUT")
print(NEAT.calcNetwork(genome1,[1,0,0]))

# mutations and calculating output are the beginnings of NEAT
# when running a normal simulation, there will be an entire generation of networks competing
# to create seperate networks from the initial network use the init
# note that these new networks will get an additional node mutation
genome2 = NEAT.mutateGenome(genome1)
genome3 = NEAT.mutateGenome(genome1)
print("\nGENOME 2")
NEAT.printGenome(genome2)
print("\nGENOME 3")
NEAT.printGenome(genome3)

# the best part about NEAT is the ability to combine networks to get new ones
# this can be done using the crossGenomes() method
genome4 = NEAT.crossGenomes(genome2,genome3)
print("\nGENOME 4")
NEAT.printGenome(genome4)