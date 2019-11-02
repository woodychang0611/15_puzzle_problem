import numpy as np
import copy, random, math


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
    def GetNeighbors(self):
        states = []
        for x,y in self.POSSIBLE_MOVES:
            try:
                new_state = copy.deepcopy(self)
                new_state.Move(x,y)
                states.append(new_state)
            except Exception:
                pass
        return states
    def Shuffle(self,steps=100):
        for _ in range(0,steps):
            x,y = State.POSSIBLE_MOVES[random.randint(0,3)]
            try:
                self.Move(x,y)
            except Exception:
                pass
    def GetHash(self):
        count =int(0)
        sum = int(0)
        for i in self.puzzle_locations.flatten('C'):
            sum += i* math.pow(16,count)
            count +=1
        return int(sum)
    def GetHeuristic(self,goal_state):
        difference_count = 0
        index = 0
        flatten_goal = goal_state.puzzle_locations.flatten('C')
        for n in self.puzzle_locations.flatten('C'):
            if (n == flatten_goal[index]):
                n=n+1
            else:
                difference_count+=1
            index+=1
        return difference_count
    def __str__(self):
        return (self.puzzle_locations.__str__())

class SearchAgent:
    def __init__(self,start_state,goal_state):
        self.start_state = start_state
        self.goal_state = goal_state
    def Start(self):
        print (self.start_state.GetHeuristic(goal_state))
        Getneighbors = start_state.GetNeighbors()
        for neighbor in Getneighbors:
            print(neighbor)

goal_state = State()
start_state = State()
start_state.Shuffle(steps = 100)
print(goal_state)
print(start_state)

  
agent = SearchAgent(start_state,goal_state)
agent.Start()