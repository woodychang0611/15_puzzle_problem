import sys
from enum import Enum
import copy
from heapq import heappush, heappop

class Node:
    def __init__(self, parent, action, state, depth: int, score: float = float("inf")):
        self.parent = parent
        self.action = action
        self.state = state
        self.depth = depth
        self.score = score

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
        if(self.mode == SearchMode.RBFS):
            self.f_limit = [sys.maxsize]
            self.alternative_node = [None]

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
            return self.problem.cost(node)
        # f(x) = h(x)
        elif (self.mode == SearchMode.Greedy_BFS):
            return self.problem.heuristic(node.state)
        # f(x) = g(x) + h(x)
        elif (self.mode == SearchMode.A_Star):
            return self.problem.cost(node)+self.problem.heuristic(node.state)
        elif (self.mode == SearchMode.RBFS):
            return self.problem.cost(node)+self.problem.heuristic(node.state)
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
        if(self.mode == SearchMode.RBFS):
            print("RBFS")
            return None

        # For Iterative-Deepening Search, stop adding frontier if the depth reach cut off depth
        if(self.mode == SearchMode.IDS and node.depth > self.cut_off_depth):
            # create a new search agent with larger cut off depth
            new_agent = copy.deepcopy(self)
            new_agent.max_queue_size = self.max_queue_size
            new_agent.cut_off_depth = self.cut_off_depth+1
            return new_agent.search()
        for successor in self.problem.get_successors(node.state):
            action,state = successor
            new_node = Node(node,action,state,node.depth+1)
            new_node.score = self.get_evaluate_value(new_node)
            self.add_frontier(new_node)
        return None

    def add_frontier(self, node):
        heappush(self.frontiers, node)
        self.max_queue_size = max(len(self.frontiers), self.max_queue_size)

    def get_next_frontier(self) -> Node:
        return heappop(self.frontiers)

    def search(self):
        root_node = Node(None, None, self.start_state, 0)
        self.add_frontier(root_node)
        while (len(self.frontiers) > 0):
            node = self.get_next_frontier()
            result = self.process_node(node)
            if (result != None):
                print(
                    f"Mode: {self.mode} Solution found!, Max queue size: {self.max_queue_size} Max depth: {node.depth}")
                return result
        print(
            f"{self.mode} Failed!, Max queue size: {self.max_queue_size} Max depth: {node.depth}")
        return None