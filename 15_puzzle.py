import numpy as np
import copy
import random

class State():
    POSSIBLE_MOVES = [(-1,0),(1,0),(0,-1),(0,1)]

    def __init__ (self):
        self.puzzle_locations = np.array([[1,2,3,4],[12,13,14,5],[11,0,15,6],[10,9,8,7]])
    def blank_location(self):
        x_blank = -1
        y_blank = -1
        for i in range(4,):
            if (0 in self.puzzle_locations[i,:]):
                y_blank =  i
            if (0 in self.puzzle_locations[:,i]):
                x_blank =  i
        return x_blank,y_blank
    def Move(self,x,y):
        x_blank,y_blank = self.blank_location()
        x_target = x_blank + x
        y_target = y_blank + y
        if(x_target <0 or x_target >3 or y_target <0 or y_target>3):
            raise Exception()
        else:
            self.puzzle_locations[y_blank,x_blank] = self.puzzle_locations[y_target,x_target]
            self.puzzle_locations[y_target,x_target] = 0
    def PossibleNextStates(self):
        states = []
        for x,y in self.POSSIBLE_MOVES:
            try:
                new_state = copy.deepcopy(self)
                new_state.Move(x,y)
                states.append(new_state)
            except Exception:
                pass
        return states
    def Shuffle(self,steps=10):
        for _ in range(0,steps):
            x,y = state.POSSIBLE_MOVES[random.randint(0,3)]
            try:
                self.Move(x,y)
            except Exception:
                pass


state = State()
print(state.puzzle_locations)
print ('------------------')



state.Shuffle(steps = 100)
print(state.puzzle_locations)

states = state.PossibleNextStates()
for s in states:
    print(s.puzzle_locations)
print ('------------------')