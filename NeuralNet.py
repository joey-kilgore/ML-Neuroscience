from random import *
import copy
import math

class NeuralNet:
    def __init__(self):
        self.layers = []

def makeNet(layerSizesOrig):
    net = NeuralNet()
    layerSizes = copy.copy(layerSizesOrig)
    layerSizes.append(1)
    layerNum = 0
    #print("Begin making layers")
    net.layers.clear()
    while layerNum<(len(layerSizes)-1):
        #print("making layer")
        newLayer = makeLayer(layerSizes[layerNum], layerSizes[layerNum+1])
        net.layers.append(copy.deepcopy(newLayer))
        #print("layer made")
        layerNum+=1
    return net

class Layer:
    def __init__(self):
        self.w = [[]]
        self.a = []

def makeLayer(cur, nex):
    #print("in makeLayer")
    layer = Layer()
    layer.w.clear()
    c = 0
    subW = []
    while c<cur:
        n = 0
        subW.clear()
        while n<nex:
            subW.append(random()*2-1)
            n+=1
        layer.w.append(copy.deepcopy(subW))
        layer.a.append(1)
        c+=1
    return layer

def printLayer(layer):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
        for row in layer.w]))

def calcNextLayer(layer):
    n = 0
    ans = []
    while n<len(layer.w[0]):
        c = 0
        sum = 0
        while c<len(layer.w):
            sum += layer.w[c][n] * layer.a[c]
            c+=1
        ans.append(squish(sum))
        n+=1
    return ans

def calcNetwork(net, input):
    net.layers[0].a = input
    layNum = 0
    while(layNum<len(net.layers)-1):
        net.layers[layNum+1].a = calcNextLayer(net.layers[layNum])
        layNum+=1
    return net.layers[-1].a

def squish(num):
    return 1 / (1 + math.exp(-num))