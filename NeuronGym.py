import neuron

h = neuron.hoc.HocObject()

class NeuronGym:      
    def __init__(self):
        self.numInputs = 101
        self.numOutputs = 2
        self.score = 0
        h('nrn_load_dll("C:/Users/Joey/Desktop/Stuff/Code/Nerve-Block-Modeling/Current Simulation/models/nrnmech.dll")')
        h('load_file("C:/Users/Joey/Desktop/Stuff/Code/Nerve-Block-Modeling/Current Simulation/CNOW_run.hoc")')
        h('electrode_api_setup()')
        h('electrode_api_change_pos(1000,-2000,2000)')
        h('init()')
        h('steprun()') # init step
        h('Tstop=50')
        self.currentTrial = -1
        self.rightSpike = 0
        self.leftSpike = 0

    def getState(self):
        self.currentTrial += 1
        inputs = []
        for i in range(101):
            inputs.append(h.node[i].v/100)
        return inputs

    def setInput(self, action):
        newCur0 = action[0]*2000000-1000000
        newCur1 = action[1]*2000000-1000000
        hocCommand = 'electrode_api_advance('+str(newCur0)+','+str(newCur1)+')'
        h(hocCommand)
        h('steprun()')
        
        # calculate score
        if (h.node[90].v > -10) and (self.rightSpike == 0):
            self.rightSpike = 1
            self.score += 1
        elif (h.node[90].v < -10) and (self.rightSpike == 1):
            self.rightSpike = 0
        if (h.node[10].v > -10) and (self.leftSpike == 0):
            self.leftSpike = 1
            self.score -= .5
        elif (h.node[10].v < -10) and (self.leftSpike == 1):
            self.leftSpike = 0
    
    def isDone(self):
        return True if self.currentTrial == 2000 else False

    def getScore(self):
        h('init()')
        h('steprun()') # init step
        pointsEarned = self.score
        self.score = 0
        self.currentTrial = -1
        return pointsEarned
