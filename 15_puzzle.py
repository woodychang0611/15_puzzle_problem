import numpy as np
import sys
import copy
import random
import math
from enum import Enum
from heapq import heappush, heappop

ACTIONS={
        'Up':(0,-1),
        'Down':(0,1),
        'Left':(-1,0),
        'Right':(1,0)
    }

class State():

    def __init__ (self):
        self.size =3
        #self.puzzle_locations = np.array([[1,2,3,4],[12,13,14,5],[11,0,15,6],[10,9,8,7]])
        self.puzzle_locations = np.array([[1,2,3],[4,5,6],[7,8,0]])
    def __eq__(self, other):
            return np.array_equal(self.puzzle_locations,other.puzzle_locations)
    def blank_location(self):
        x_blank = -1
        y_blank = -1
        for i in range(self.size,):
            if (0 in self.puzzle_locations[i,:]):
                y_blank =  i
            if (0 in self.puzzle_locations[:,i]):
                x_blank =  i
        return x_blank,y_blank
    def move(self,action):
        shape = list(self.puzzle_locations.shape)
        x_size = shape[1]
        y_size = shape[0]
        x,y = ACTIONS[action]
        x_blank,y_blank = self.blank_location()
        x_target = x_blank + x
        y_target = y_blank + y
        if(x_target <0 or x_target > self.size -1 or y_target <0 or y_target> self.size-1):
            raise Exception()
        else:
            self.puzzle_locations[y_blank,x_blank] = self.puzzle_locations[y_target,x_target]
            self.puzzle_locations[y_target,x_target] = 0
    def get_neighbors(self):
        states = []
        for action in ACTIONS:
            try:
                new_state = copy.deepcopy(self)
                new_state.move(action)
                states.append(new_state)
            except Exception:
                pass
        return states
    def shuffle(self,steps=100):
        for _ in range(0,steps):
            action= random.choice(list(ACTIONS.keys()))
            try:
                self.move(action)
            except Exception:
                pass
    def get_hash(self):
        count =int(0)
        sum = int(0)
        for i in self.puzzle_locations.flatten('C'):
            sum += i* (self.size**2)**count
            count +=1
        return int(sum)
    def get_heuristic(self):
        difference_count = 0
        index = 0
        flatten_goal = State().puzzle_locations.flatten('C')
        for n in self.puzzle_locations.flatten('C'):
            if (n == flatten_goal[index]):
                n=n+1
            else:
                difference_count+=1
            index+=1
        return difference_count
    def is_failed(self):
        return False
    
    def __str__(self):
        return (self.puzzle_locations.__str__())


class Node:
     def __init__(self,parent,state,depth:int,score:float):
         self.parent = parent
         self.state = state
         self.depth = depth
         self.score = score
     #This is needed for heap queue
     def __lt__(self, other):
         return self.score < other.score
     def __le__(self, other):
         return self.score < other.score

class SearchMode(Enum):
     IDS =0
     UCS=1
     Greedy_BFS=2
     A_Star=3
     RBFS=4

class SearchAgent:
    def __init__(self,start_state,goal_check_function,mode:SearchMode):
        self.start_state = start_state
        self.goal_check_function = goal_check_function
        self.explored={}
        self.frontiers=[]
        self.mode = mode
        self.max_queue_size = len(self.frontiers)
        if(self.mode == SearchMode.IDS):
            self.cut_off_depth =1
        if(self.mode == SearchMode.RBFS):
            self.f_limit = [sys.maxsize]
            self.alternative_node = [None]
    
    def get_evaluate_value(self,state,depth):
        #use a smaller number so it works like stack
        if(self.mode == SearchMode.IDS):
            if (len (self.frontiers)==0):
                self.stack_count=0
                return 0
            else:
                self.stack_count-=1
                return self.stack_count 
                #return min(self.frontiers).score-1
        #f(x) = g(x)
        elif (self.mode == SearchMode.UCS):
            return depth
        #f(x) = h(x)    
        elif (self.mode == SearchMode.Greedy_BFS):
            return state.get_heuristic()
        #f(x) = g(x) + h(x)   
        elif (self.mode == SearchMode.A_Star):
            return depth+state.get_heuristic()
        elif (self.mode == SearchMode.RBFS):
            return depth+state.get_heuristic()  
        return 0

    def process_node(self,node:Node):
        state = node.state
        hash = state.get_hash()
        if (self.goal_check_function(state)):
            return node
        if (hash in self.explored.keys()):
            return None
        if (state.is_failed()):
            return None
        self.explored[hash] = node
        if(self.mode == SearchMode.RBFS):
            print ("RBFS")          
            return None

        #For Iterative-Deepening Search, stop adding frontier if the depth reach cut off depth
        if(self.mode == SearchMode.IDS and node.depth > self.cut_off_depth):
            return None
        neighbors = state.get_neighbors()
        for neighbor in neighbors:
            score = self.get_evaluate_value(neighbor,node.depth+1)
            new_node = Node(node,neighbor,node.depth+1,score)
            self.add_frontier(new_node)
        return None

    def add_frontier(self,node):
        heappush(self.frontiers,node)
        self.max_queue_size = max(len(self.frontiers),self.max_queue_size)

    def get_next_frontier(self) -> Node:
        return heappop(self.frontiers)

    def search(self):
        root_node = Node(None,self.start_state,0,float("inf"))
        self.add_frontier(root_node)
        while (len(self.frontiers)>0):
            node = self.get_next_frontier()
            result = self.process_node (node)
            if (result != None):
                print (f"Mode: {self.mode} Solution found!, Max queue size: {self.max_queue_size} Max depth: {node.depth}")
                return result
        #For IDS, recursiely call a new IDS search agent with cut_off_depth+1
        if(self.mode == SearchMode.IDS):
            new_cut_off_depth = self.cut_off_depth+1
            max_queue_size = self.max_queue_size
            #reset the search agent
            new_agent = SearchAgent(self.start_state,self.goal_check_function,self.mode)
            new_agent.max_queue_size = max_queue_size
            new_agent.cut_off_depth = new_cut_off_depth
            return new_agent.search()
        print (f"{self.mode} Failed!, Max queue size: {self.max_queue_size} Max depth: {node.depth}")
        return None


goal_state = State()
start_state =  State()
start_state.shuffle(steps = 10)
print('Goal State')
print(goal_state)
print('Start State')
print(start_state)


#agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.RBFS)
#solution_node = agent.search()
#exit(0)

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.Greedy_BFS)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.A_Star)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.UCS)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.IDS)
solution_node = agent.search()    