import NeuralNet as NN
import copy
from random import *

def trainNet(sizeOfNet, testFunc, numGenerations):
    # make initial set of 300 nets
    nets = []
    for i in range(100):
        nets.append(NN.makeNet(sizeOfNet))
    print("INIT NETS MADE")
    absMax = 0
    bestNet = NN.makeNet(sizeOfNet)
    bestNets = []
    bestScores = []
    for gen in range(numGenerations):
        testScores = testFunc(nets)
        avgScore = 0
        bestGenScore = -10
        for i in range(100):
            avgScore+=testScores[i]
            if testScores[i] > absMax:
                absMax = testScores[i]
                bestNet = nets[i]
            if testScores[i] > bestGenScore:
                bestGenScore = testScores[i]
        avgScore = avgScore/100
        print("AVG SCORE GEN:"+str(gen)+ " is " + str(avgScore))
        print("BEST SCORE GEN:" + str(bestGenScore))
        print("BEST SCORE OVERALL:" + str(absMax))
        #nets.extend(bestNets)
        #testScores.extend(bestScores)
        bestNets = []
        bestScores = []
        #oldNets = nets
        topScoreIndex = []
        for i in findTopScores(testScores, nets):
            bestNets.append(nets[i])
            bestScores.append(testScores[i])
        
        #for i in testFunc(bestNets):
        #    print(i)

        nets = nextGen(sizeOfNet, bestNets)
        #nets.extend(bestNets)

def nextGen(sizeOfNet, bestNets):
    newNets = []
    for i in range(100):
        newNets.append(NN.makeNet(sizeOfNet))
        #print("WEIGHT UPDATE:" + str(i))
        if(i/10 == int(i/10)):
            newNets[i] = bestNets[int(i/10)]
        else:
            parentNet = bestNets[int(i/10)]
            for l in range(len(parentNet.layers)):
                # make new weights
                for wArr in range(len(parentNet.layers[l].w)):
                    for wInd in range(len(parentNet.layers[l].w[wArr])):
                        newNets[i].layers[l].w[wArr][wInd] = parentNet.layers[l].w[wArr][wInd] + (random()-.5)/10
    return newNets

def findTopScores(scores, nets):
    #print("FINDING TOP SCORES")
    numScores = 10
    bestScores = []
    for i in range(numScores):
        topScore = -10000000000
        topIndex = 0
        for j in range(len(scores)):
            if ((scores[j])>topScore)and(not(j in bestScores)):
                topScore = scores[j]
                topIndex = j
        bestScores.append(topIndex)
        #print("SCORE FOUND " + str(i))
    return bestScores

