import neuron
import NeuralNet as NN
import time

h = neuron.hoc.HocObject()
h('nrn_load_dll("C:/Users/Joey/Desktop/Stuff/Code/Nerve-Block-Modeling/Current Simulation/models/nrnmech.dll")')
h('load_file("C:/Users/Joey/Desktop/Stuff/Code/Nerve-Block-Modeling/Current Simulation/CNOW_run.hoc")')

baseLineRunTime = 0

def neuronTest(nets):
    global baseLineRunTime
    scores = []
    progress = 0
    printProgressBar(0, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
    startTime = time.time()
    leftSpike = 0
    rightSpike = 0
    for net in nets:
        h('init()')
        h('steprun()') # init step
        score = 0
        for steps in range(10000):
            # gather inputs
            inputs = []
            for i in range(101):
                inputs.append(h.node[i].v/100)
            # feed input in network
            output = NN.calcNetwork(net, inputs)
            # set extracellular voltage from NN output
            newCurrent1 = output[0]*2000000 - 1000000
            newCurrent2 = output[1]*2000000 - 1000000
            #print(newVolt)
            hocCommand = 'electrode_api_advance('+str(newCurrent1)+','+str(newCurrent2)+')'
            h(hocCommand)
            # take a single time step
            h('steprun()')
            # calc score
            if (h.node[90].v > -10) and (rightSpike == 0):
                rightSpike = 1
                score += 1
            if (h.node[90].v < -10) and (rightSpike == 1):
                rightSpike = 0
            if (h.node[10].v > -10) and (leftSpike == 0):
                leftSpike = 1
                score += 1
            if (h.node[10].v < -10) and (leftSpike == 1):
                leftSpike = 0
                
        scores.append(score)
        progress+=1
        printProgressBar(progress, 100, prefix = 'Progress:', suffix = 'Complete', length = 50)
    endTime = time.time()
    runTime = endTime - startTime
    if baseLineRunTime == 0:
        baseLineRunTime = runTime
    if runTime > baseLineRunTime+20:
        setEnvironment()
    
    print("TOTAL TIME: " + str(endTime-startTime))
    return scores



def setEnvironment():
    h('electrode_api_setup()')
    h('electrode_api_change_pos(1000,-2000,2000)')

setEnvironment()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()