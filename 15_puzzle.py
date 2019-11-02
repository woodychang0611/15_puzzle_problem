import numpy as np
import copy, random, math
from enum import Enum
from heapq import heappush, heappop

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


class Node:
     def __init__(self,parent,value,depth:int):
         self.parent = parent
         self.value = value
         self.depth=depth
     def __lt__(self, other):
         return False
     def __le__(self, other):
         return False

class SearchMode(Enum):
     A_Star =0
     IDS =1
class Test:
    def __init__(self):
        pass
class SearchAgent:
    
    def __init__(self,start_state,goal_check_function,mode:SearchMode):
        self.start_state = start_state
        self.goal_check_function = goal_check_function
        #Dictionary
        self.explored={}
        #Priority Queue
        print('set frontiers')
        self.frontiers=[]
        self.mode = mode
    
    def get_evaluate_value(self,node):
        return node.depth       
    def process_node(self,Node): 
        pass
    def add_frontier(self,node):
        evaluate_value = self.get_evaluate_value(node)
        print (self.frontiers)
        #self.frontiers = []
        heappush(self.frontiers,(evaluate_value,node))
    def get_next_frontier(self) -> Node:
        return heappop(self.frontiers)[1]

    def start(self):
        start_node = Node(None,self.start_state,0)
        self.add_frontier(start_node)
        neighbors = start_node.value.GetNeighbors()
        for neighbor in neighbors:
            node = Node(start_node,neighbor,1)
            self.add_frontier(node)
        

        print (len(self.frontiers))
        while (len(self.frontiers) > 0):
            node = self.get_next_frontier()
            print('='*80)
            print(node.depth)
            print(node.value)





goal_state = State()
start_state = State()
start_state.Shuffle(steps = 100)
print(goal_state)
print(start_state)

  
agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.IDS)
print (agent.start())
