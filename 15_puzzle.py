import numpy as np
import sys
import copy
import random
import math

from SearchAgent import SearchAgent,SearchMode

class PuzzleState:
    def __init__(self, puzzle_locations):
        self.puzzle_locations = puzzle_locations
        shape = puzzle_locations.shape
        self.x_size = shape[1]
        self.y_size = shape[0]

    def blank_location(self):
        x_blank = -1
        y_blank = -1
        for i in range(0, self.y_size):
            if (0 in self.puzzle_locations[i, :]):
                y_blank = i
        for i in range(0, self.x_size):
            if (0 in self.puzzle_locations[:, i]):
                x_blank = i
        return x_blank, y_blank

    def get_hash(self):
        count = int(0)
        sum = int(0)
        for i in self.puzzle_locations.flatten('C'):
            sum += i * (self.x_size*self.y_size)**count
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
        return node.depth
    def heuristic(self,state):
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
        x_blank, y_blank = new_state.blank_location()
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

#goal_locations = np.array(
#    [[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]])
goal_locations = np.array([[1,2,3],[4,5,6],[7,8,0]])

goal_state = PuzzleState(goal_locations)
start_state = PuzzleProblem.shuffle(goal_state, 2)
problem = PuzzleProblem(goal_state)
print('Goal State')
print(goal_state)
print('Start State')
print(start_state)

agent = SearchAgent(start_state, problem, SearchMode.UCS)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.Greedy_BFS)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.A_Star)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.IDS)
solution_node = agent.search()
exit(0)