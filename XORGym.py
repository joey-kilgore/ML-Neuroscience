class XORGym:
    # This class functions as a reference for building new gyms
    # Gyms are used with NEAT to use machine learning to find optimum ways to score points in the gym
    # This gym uses the classic XOR problem (https://www.quora.com/What-is-XOR-problem-in-neural-networks)
    # When building your own gym knowing the flow of training is important
    # A trial consists of getting the state and setting input
    # First getState is called
    #   This means the state should be set at initialization and reset at the end of the trial
    #   This is where the trial count is incremented
    # Second setInput is called
    #   This is where input is set from the subject and then the score is incremented based off of the input
    # Third isDone is called
    #   This is the flag used to ensure the subject goes through the correct number of trials
    # Steps 1-3 are repeated as necesary
    # Finally getScore is called
    #   This returns the score, and resets the training environment
    def __init__(self):
        # The NECESARY components of the constructor are the numInputs and numOutputs
        self.numInputs = 3      # NEED TO INCLUDE   (3 inputs - 2 from the XOR inputs, 1 bias)
        self.numOutputs = 1     # NEED TO INCLUDE   (1 output - the value of the XORed inputs)
        self.score = 0          # used to keep track of score across trails
        self.states = [[0,0], [0,1], [1,0], [1,1]]  # these are the 4 possible states
        self.stateValue = [0,1,1,0] # the XOR of the 4 possible states
        self.currentTrial = -1  # the initial trial is set

    def getState(self):
        self.currentTrial += 1  # increment the trial
        state = [1]             # add the bias
        state.extend(self.states[self.currentTrial])    # add the state
        return state

    def setInput(self, action):
        # the action is a list given from the subject
        # points are awarded for getting closer to the actual value of the inputs XORed (maximum of 1 point)
        self.score += 1 - abs(self.stateValue[self.currentTrial] - action[0])

    def isDone(self):
        # check if the fourth trial has been completed
        if self.currentTrial == 3: 
            return True
        return False
    
    def getScore(self):
        # get the score earned and reset the training environment
        pointsEarned = self.score
        self.score = 0
        self.currentTrial = -1
        return pointsEarned