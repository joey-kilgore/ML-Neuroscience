import NeuralNet as NN
import random
import Train
import NeuronTestEnvironment as NTE

def testGame(nets):
    # TEST GAME FOR NET
    # 3 outputs, 1 is worth 2 points, 2 are worth -1
    # 1 input, telling where the 2 point output is
    scores = []
    for net in nets:
        totalScore = 0
        points = [2,-1,-1]
        for trial in range(10):
            #random.shuffle(points)
            prize = 0
            for i in range(len(points)):
                if points[i] == 2:
                    prize = i
            inputs = []
            inputs.append(prize-1)      
            output = NN.calcNetwork(net,inputs)
            score = 0
            for i in range(len(output)):
                score += output[i]*points[i]
            totalScore += score
        totalScore = totalScore/10
        scores.append(totalScore)
    return scores

NTE.setEnvironment()
Train.trainNet([101,20,20,2], NTE.neuronTest, 100)