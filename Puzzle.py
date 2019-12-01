import math
import random
import copy
import numpy as np

class PuzzleState:
    def __init__(self, puzzle_locations):
        self.puzzle_locations = puzzle_locations
        shape = puzzle_locations.shape
        self.y_size = shape[0]        
        self.x_size = shape[1]

    def get_location(self,label):
        x = -1
        y = -1
        for i in range(0, self.y_size):
            if (label in self.puzzle_locations[i, :]):
                y = i
        for i in range(0, self.x_size):
            if (label in self.puzzle_locations[:, i]):
                x = i
        return x, y

    def get_hash(self):
        count = int(0)
        sum = int(0)
        for i in self.puzzle_locations.flatten('C'):
            sum += i * math.pow((self.x_size*self.y_size),count)
            count += 1
        return int(sum)

    def __str__(self):
        return (self.puzzle_locations.__str__())

    def __eq__(self, other):
        if(other == None):
            return False
        return np.array_equal(self.puzzle_locations, other.puzzle_locations)


class PuzzleProblem:
    ACTIONS = {
        'Up': (0, -1),
        'Down': (0, 1),
        'Left': (-1, 0),
        'Right': (1, 0)
    }
    def __init__ (self,goal_state):
        self.goal_state = goal_state
    def test_goal(self,state): 
        return state == self.goal_state
    def cost(self,node):
        if (node.parent == None):
            return 1
        return node.parent.cost+1
    #Manhatten
    def heuristic(self,state):
        flatten_state = self.goal_state.puzzle_locations.flatten('C')
        sum=0
        for label in flatten_state:
            x_goal,y_goal = self.goal_state.get_location(label)
            x_state,y_state = state.get_location(label)
            sum+=abs(x_goal-x_state)+(y_goal-y_state)
        return sum

    def heuristic2(self,state):
        difference_count = 0
        index = 0
        flatten_goal = self.goal_state.puzzle_locations.flatten('C')
        for n in state.puzzle_locations.flatten('C'):
            if (n == flatten_goal[index]):
                n = n+1
            else:
                difference_count += 1
            index += 1
        return difference_count
    def test_fail(self,state): 
        return False
    def get_successors(self,state):
        result=[]
        for key in PuzzleProblem.ACTIONS.keys():
            action = key
            new_state =PuzzleProblem.transition(state,action)
            if(new_state != None):
                result.append((action,new_state))
        return result
    @staticmethod
    def transition(state: PuzzleState, action):
        new_state = copy.deepcopy(state)
        x_mov, y_mov = PuzzleProblem.ACTIONS[action]
        x_blank, y_blank = new_state.get_location(0)
        x_target = x_blank + x_mov
        y_target = y_blank + y_mov
        if(x_target < 0 or x_target > state.x_size - 1 or y_target < 0 or y_target > state.y_size-1):
            return None
        else:
            new_state.puzzle_locations[y_blank,
                                       x_blank] = new_state.puzzle_locations[y_target, x_target]
            new_state.puzzle_locations[y_target, x_target] = 0
        return new_state

    @staticmethod
    def shuffle(state, steps):
        count = 0
        shuffled_state = state
        while (count < steps):
            action = random.choice(list(PuzzleProblem.ACTIONS.keys()))
            new_state = PuzzleProblem.transition(shuffled_state, action)
            if(new_state != None):
                shuffled_state = new_state
                count += 1
        return shuffled_state