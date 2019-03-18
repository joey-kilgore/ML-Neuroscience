class XORGym:
    
    def __init__(self):
        self.numInputs = 3
        self.numOutputs = 1
        self.score = 0
        self.states = [[0,0], [0,1], [1,0], [1,1]]
        self.stateValue = [0,1,1,0]
        self.currentTrial = -1

    def getState(self):
        self.currentTrial += 1
        state = [1]
        state.extend(self.states[self.currentTrial])
        return state

    def setInput(self, action):
        if (action > 0.5 and self.stateValue[self.currentTrial] == 1) or (action < 0.5 and self.stateValue[self.currentTrial] == 0):
            self.score += 1

    
    def isDone(self):
        if self.currentTrial == 3:
            self.currentTrial = -1
            return True
        return False
    
    def getScore(self):
        pointsEarned = self.score
        self.score = 0
        return pointsEarned