import numpy as np
from SearchAgent import SearchAgent,SearchMode
from  Puzzle import PuzzleProblem,PuzzleState


#goal_locations = np.array([[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]])
goal_locations = np.array([[1,2,3],[4,5,6],[7,8,0]])

goal_state = PuzzleState(goal_locations)
start_state = PuzzleProblem.shuffle(goal_state,10)


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

agent = SearchAgent(start_state, problem, SearchMode.RBFS)
solution_node = agent.search()