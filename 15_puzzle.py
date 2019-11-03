import numpy as np
import sys, copy, random, math
from enum import Enum
from heapq import heappush, heappop

class State():
    POSSIBLE_MOVES = [(-1,0),(1,0),(0,-1),(0,1)]
    def __init__ (self):
        self.puzzle_locations = np.array([[1,2,3,4],[12,13,14,5],[11,0,15,6],[10,9,8,7]])
    def __eq__(self, other):
            return np.array_equal(self.puzzle_locations,other.puzzle_locations)
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
    def GetHeuristic(self):
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
    def IsFailed(self):
        return False
    def __str__(self):
        return (self.puzzle_locations.__str__())


class Node:
     def __init__(self,parent,value,depth:int):
         self.parent = parent
         self.value = value
         self.depth=depth
     #This is needed for heap queue
     def __lt__(self, other):
         return False
     def __le__(self, other):
         return False

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
    
    def get_evaluate_value(self,node):
        #use a smaller number so it works like stack
        if(self.mode == SearchMode.IDS):
            if (len (self.frontiers)==0):
                return 0
            else:
                return min(self.frontiers)[0]-1
        #f(x) = g(x)
        elif (self.mode == SearchMode.UCS):
            return node.depth
        #f(x) = h(x)    
        elif (self.mode == SearchMode.Greedy_BFS):
            return node.value.GetHeuristic()
        #f(x) = g(x) + h(x)      
        elif (self.mode == SearchMode.A_Star):
            return node.depth+node.value.GetHeuristic()
        elif (self.mode == SearchMode.RBFS):
            return node.depth+node.value.GetHeuristic()  
        return 0

    def process_node(self,node:Node):
        state = node.value
        hash = state.GetHash()
        if (self.goal_check_function(state)):
            return node
        if (hash in self.explored.keys()):
            return None
        if (state.IsFailed()):
            return None
        self.explored[hash] = node
        if(self.mode == SearchMode.RBFS):
            print ("RBFS")
            neighbors = state.GetNeighbors()
            child_nodes =[]
            for n in neighbors:
                child_node = Node(node,n,node.depth+1)
                evaluate_value = self.get_evaluate_value(child_node)
                child_nodes.append((evaluate_value,child_node))
            child_nodes.sort()

            #get highest
            next_node = child_nodes[0][1]
            alternative_node = child_nodes[1][1]
            print(self.get_evaluate_value(next_node))
            print(next_node.value)
            print(self.get_evaluate_value(alternative_node))
            print(alternative_node.value)            
            return None

        #For Iterative-Deepening Search, stop adding frontier if the depth reach cut off depth
        if(self.mode == SearchMode.IDS and node.depth >= self.cut_off_depth):
            return None
        neighbors = state.GetNeighbors()
        for neighbor in neighbors:
            new_node = Node(node,neighbor,node.depth+1)
            self.add_frontier(new_node)
        return None

    def add_frontier(self,node):
        evaluate_value = self.get_evaluate_value(node)
        heappush(self.frontiers,(evaluate_value,node))
        self.max_queue_size = max(len(self.frontiers),self.max_queue_size)
    def get_next_frontier(self) -> Node:
        return heappop(self.frontiers)[1]

    def search(self):
        root_node = Node(None,self.start_state,0)
        self.add_frontier(root_node)
        while (len(self.frontiers)>0):
            node = self.get_next_frontier()
            result = self.process_node (node)
            if (result != None):
                print (f"Mode: {self.mode} Solution found!, Max queue size: {self.max_queue_size} Max depth: {node.depth}")
                return result
        if(self.mode == SearchMode.IDS):
            new_cut_off_depth = self.cut_off_depth+1
            #reset the search agent
            self = SearchAgent(self.start_state,self.goal_check_function,self.mode)
            self.cut_off_depth = new_cut_off_depth
            return self.search()
        print ("Fail!")
        return None


goal_state = State()
start_state =  State()
start_state.Shuffle(steps = 20)
print('Goal State')
print(goal_state)
print('Start State')
print(start_state)


agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.RBFS)
solution_node = agent.search()
exit(0)

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.Greedy_BFS)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.A_Star)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.UCS)
solution_node = agent.search()

agent = SearchAgent(start_state,lambda s:s== goal_state,SearchMode.IDS)
solution_node = agent.search()

