import numpy as np
from SearchAgent import SearchAgent,SearchMode
from  Puzzle import PuzzleProblem,PuzzleState

goal_locations = np.array([[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]])
#goal_locations = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
#goal_locations = np.array([[1,2,3],[8,0,4],[7,6,5]])

#start_locations =np.array([[1, 2, 3, 4], [12, 13, 14, 5], [0, 11, 15, 6], [10, 9, 8, 7]])
#start_locations =np.array([[15, 2, 1, 12], [8, 5,6, 11], [4, 9, 10, 7], [3, 14, 13, 0]])
start_locations =np.array([[1, 2, 3, 4], [12, 13,14, 5], [10, 11, 7, 8], [9, 0, 6, 15]])
#start_locations =np.array([[8, 3, 5],[4, 1, 6], [2, 7, 0]])

start_state = PuzzleState(start_locations)
goal_state = PuzzleState(goal_locations)

#start_state = PuzzleProblem.shuffle(goal_state,21)

problem = PuzzleProblem(goal_state)

print('Goal State')
print(goal_state)
print('Start State')
print(start_state)

agent = SearchAgent(start_state, problem, SearchMode.A_Star)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.Greedy_BFS)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.UCS)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.RBFS)
solution_node = agent.search()

agent = SearchAgent(start_state, problem, SearchMode.IDS)
solution_node = agent.search()
