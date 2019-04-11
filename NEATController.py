import NEAT
import XORGym
import random
import copy
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

def test(genome, gym):
    # test the genome in the gym
    # return the score the genome achieved
    gymCopy = copy.deepcopy(gym)
    while not gymCopy.isDone():
        gymCopy.setInput(NEAT.sigmoidActivationFunction(10 * NEAT.calcNetwork(genome, gymCopy.getState())[0]))
    score = gymCopy.getScore()
    return score


def makeNextGen(i, bestGenomes, sizeOfGenerations):
    # make a new genome from the best genomes
    # half of genomes will be a cross of two parents, and half will be a mutation of one genome
    if i < sizeOfGenerations/4:
        parents = findParents(bestGenomes)
        return NEAT.crossGenomes(parents[0],parents[1])
    else:
        return NEAT.mutateGenome(random.choice(bestGenomes))

def train(gym, numGenerations, sizeOfGenerations):
    # based on only a gym, generations are created to maximize their performance

    # the initial genome is the first genome created and needs to be created seperately
    initGenome = NEAT.initGenome(gym.numInputs, gym.numOutputs)
    generation = [initGenome]

    bestScore = 0
    bestGenome = None

    # the first generation is collection of mutations on the initial genome
    for i in range(sizeOfGenerations):
        generation.append(NEAT.mutateGenome(initGenome))

    for gen in range(numGenerations):
        # for each generation we do the following
        
        # test every genome in the generation and keep track of their scores
        scores = []
        for genome in generation:
            scores.append(test(genome,gym))

        # if a new max score was reached, then it is recorded and the genome is saved
        for i in range(len(scores)):
            if scores[i] > bestScore:
                bestGenome = generation[i]
                bestScore = scores[i]
       
        # compare the generation and find the top 10%
        topGenomes = findTopGenomes(scores, generation)

        # create the next generation from the best of the current generation
        generation = []
        for i in range(sizeOfGenerations):
            generation.append(makeNextGen(i,topGenomes,sizeOfGenerations))

        # output performance metrics 
        printGenerationStats(gen,scores, bestScore, bestGenome, gym)
    return bestGenome
    
def findTopGenomes(origscores, origgeneration):
    scores = copy.copy(origscores)
    generation = copy.deepcopy(origgeneration)
    topGenomes = []
    for i in range(int(len(generation)/10)):
        topScore = 0
        topGenome = None
        for j in range(len(scores)):
            if scores[j] > topScore:
                topScore = scores[j]
                topGenome = generation[j]
        topGenomes.append(topGenome)
        scores.remove(topScore)
        generation.remove(topGenome)
    return topGenomes

def findParents(topGenomes):
    found = False
    while not found:
        parent1 = random.choice(topGenomes)
        parent2 = random.choice(topGenomes)
        if parent1 != parent2:
            found = True
    return [parent1, parent2]

def printGenerationStats(gen, scores, bestScore, bestGenome, gym):
    print("\nGEN " + str(gen))
    avg = 0
    for score in scores:
        avg += score
    avg /= len(scores)
    print("AVG " + str(avg))
    print("BEST " + str(bestScore))
    NEAT.printGenome(bestGenome)
    while not gym.isDone():
        state = gym.getState()
        setValues = NEAT.calcNetwork(bestGenome, state)
        setValue = NEAT.sigmoidActivationFunction(10*setValues[0])
        gym.setInput(setValue)
        print(str(state) + " -> " + str(setValue))
    score = gym.getScore()


testGym = XORGym.XORGym()
genome = train(testGym, 100, 100)
# while not testGym.isDone():
#     state = testGym.getState()
#     print("STATE " + str(state))
#     nextInput = NEAT.calcNetwork(genome, state)
#     print("OUTPUT " + str(nextInput))
#     testGym.setInput(nextInput)
# print(testGym.getScore())
print("BEST SCORE")
print(test(genome, testGym))