import sys
from enum import Enum
from heapq import heappush, heappop

class Node:
    def __init__(self, parent, action, state, depth: int, score: float = float("inf"), cost: float = float("inf")):
        self.parent = parent
        self.action = action
        self.state = state
        self.depth = depth
        self.score = score
        self.cost = cost
    def get_neighbors(self):
        neighbors=[]
        return neighbors
     # This is needed for heap queue

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

class SearchMode(Enum):
    IDS = 0
    UCS = 1
    Greedy_BFS = 2
    A_Star = 3
    RBFS = 4

class SearchAgent:
    def __init__(self, start_state, problem, mode: SearchMode):
        self.start_state = start_state
        self.problem = problem
        self.explored = {}
        self.frontiers = []
        self.mode = mode
        self.max_queue_size = len(self.frontiers)
        if(self.mode == SearchMode.IDS):
            self.cut_off_depth = 1
            self.cut_off_depth_reached = False

    def get_evaluate_value(self, node):
        # return a smaller number so it works like stack
        if(self.mode == SearchMode.IDS):
            if (len(self.frontiers) == 0):
                self.stack_count = 0
                return 0
            else:
                self.stack_count -= 1
                return self.stack_count
        # f(x) = g(x)
        elif (self.mode == SearchMode.UCS):
            return node.cost
        # f(x) = h(x)
        elif (self.mode == SearchMode.Greedy_BFS):
            return node.heuristic
        # f(x) = g(x) + h(x)
        elif (self.mode == SearchMode.A_Star):
            return node.cost+node.heuristic
        elif (self.mode == SearchMode.RBFS):
            return node.cost+node.heuristic
        return 0

    def process_node(self, node: Node):
        state = node.state
        hash = state.get_hash()
        if (self.problem.test_goal(state)):
            return node
        if (hash in self.explored.keys()):
            return None
        if (self.problem.test_fail(node)):
            return None
        self.explored[hash] = node

        # For Iterative-Deepening Search, stop adding frontier if the depth reach cut off depth
        if(self.mode == SearchMode.IDS and node.depth >= self.cut_off_depth):
            # create a new search agent with larger cut off depth
            self.cut_off_depth_reached=True
            return None
        new_nodes =[]
        for successor in self.problem.get_successors(node.state):
            action,state = successor
            new_node = Node(node,action,state,node.depth+1)
            new_node.cost = self.problem.cost(new_node)
            new_node.heuristic = self.problem.heuristic(new_node.state)
            new_node.score = self.get_evaluate_value(new_node)
            new_nodes.append(new_node)
        for new_node in new_nodes:
            self.add_frontier(new_node)
        return None

    def add_frontier(self, node):
        heappush(self.frontiers, node)
        self.max_queue_size = max(len(self.frontiers), self.max_queue_size)

    def get_next_frontier(self) -> Node:
        return heappop(self.frontiers)
    def process_rbfs(self,node,f_limit):
        if (self.problem.test_goal(node.state)):
            return node,-1
        new_nodes=[]
        for successor in self.problem.get_successors(node.state):
            action,state = successor
            new_node = Node(node,action,state,node.depth+1)
            new_node.cost = self.problem.cost(new_node)
            new_node.heuristic = self.problem.heuristic(new_node.state)
            new_node.score = self.get_evaluate_value(new_node)
            new_node.f = max(new_node.score,node.f)
            new_nodes.append(new_node)
        if (len(new_nodes)==0):
            return None,float('inf')
        while (len(new_nodes)>0):
            new_nodes.sort(key=lambda n:n.f)
            best = new_nodes[0]
            if(best.f > f_limit):
                return None,best.f
            if (len(new_nodes)>=2):
                alternative = new_nodes[1].f
            else:    
                alternative = float('inf')
            result,best.f = self.process_rbfs(best,min(f_limit,alternative))
            if(result!=None):
                return result,-1
        return None,float('inf')

    def search(self):
        root_node = Node(None, None, self.start_state,0,cost=0)
        if(self.mode == SearchMode.RBFS):
            root_node.f = 0
            solution_node,_ = self.process_rbfs(root_node,float('inf'))
        else:
            self.add_frontier(root_node)
            while (len(self.frontiers) > 0):
                frontier_node = self.get_next_frontier()
                solution_node = self.process_node(frontier_node)
                if(solution_node != None):
                    break
        if (solution_node != None):
            print(
                f"Mode: {self.mode} Solution found!, Max queue size: {self.max_queue_size} Max depth: {solution_node.depth}")
            actions =[]
            node = solution_node
            while (node!=None):
                actions.append(node.action)
                node = node.parent
            actions.reverse()
            #Skip root action                           
            actions = actions[1:]
            print (actions)
            return solution_node
        if(self.mode == SearchMode.IDS and self.cut_off_depth_reached):
        #create a new search agent with larger cut off depth
            new_agent = SearchAgent(self.start_state,self.problem,self.mode)
            new_agent.max_queue_size = self.max_queue_size
            new_agent.cut_off_depth = self.cut_off_depth+1
            return new_agent.search()
        print(f"{self.mode} Failed!, Max queue size: {self.max_queue_size}")
        return None