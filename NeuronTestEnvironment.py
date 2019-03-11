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
    for net in nets:
        h('init()')
        h('steprun()') # init step
        score = 0
        for steps in range(300):
            # gather inputs
            inputs = []
            inputs.append(.8) # m value wanted
            #inputs.append(.8) # h value wanted
            inputs.append(h.node[50].m_axnode)  # actual m value
            inputs.append(h.node[50].h_axnode)  # actual h value
            inputs.append(h.node[50].mp_axnode) # actual n value
            inputs.append(h.node[50].s_axnode)  # actual s value
            inputs.append(h.node[50].v)
            # feed input in network
            output = NN.calcNetwork(net, inputs)
            # set extracellular voltage from NN output
            newCurrent = output[0]*2000000 - 1000000
            #print(newVolt)
            hocCommand = 'electrode_api_advance('+str(newCurrent)+')'
            h(hocCommand)
            # take a single time step
            h('steprun()')
            # calc score
            score += 1-abs(.8-h.node[50].m_axnode)#-abs(.8-h.node[50].h_axnode)
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
    h.amp1 = 0
    h('sinestim()')
    h('setStim(0,0,0)')
    h('tstop = 5')
    h('wavesel[1] = 0')

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