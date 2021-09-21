# algorithm for solving sliding puzzle
import numpy as np
import heapq
from memory_profiler import profile
# from puzzle import *
import puzzle

'''
the listed algorithms are implemented: 
- Breadth-First Search
- Depth Limited Search
- Heuristic Search (use A* algorithm)

they followd the definition pattern as followed: 
    def search(state: numpy.ndarray) -> action_seq: Optional[list[numpy.ndarray]] = None:
        ...
if solution is found, the action sequence(e.g., [[0, -1], [1, 0], ...]) is returned
if solution is not fouund, None is returned

'''



# Breadth-First Search
# if solution is found, return the solution's action sequence
# if not found, return None
def bfs(src_state):
    queue, state_visited = [], {}
    # stringize the state(numpy.ndarray) to make it hashable
    state_visited[str(src_state)] = True
    queue.append({'state': src_state, 'action_seq': []})
    
    while len(queue) > 0:
        now, queue = queue[0], queue[1:]
        now_state, now_action_seq = now['state'], now['action_seq']
        assert isinstance(now_state, np.ndarray)
        
        # found
        if puzzle.is_equal(now_state, puzzle.tgt_state):
            return now_action_seq
        
        # not found, continue to explore
        for action in puzzle.get_action_space(now_state):
            next_state, next_action_seq = puzzle.get_next_state(now_state, action), now_action_seq + [action]
            if str(next_state) in state_visited:
                continue
            state_visited[str(next_state)] = True
            queue.append({'state': next_state, 'action_seq': next_action_seq})
    
    # not found
    return None


# Depth Limited Search
# if solution is found, return the solution's action sequence
# if not found, return None
def dfs(src_state, depth_limit=99):
    # store the depth of visited node for comparison
    state_visited = {}

    # internal recursive function
    def _dfs(state, action_seq=[]):
        nonlocal state_visited, depth_limit
        
        if puzzle.is_equal(state, puzzle.tgt_state):
            # found
            return action_seq
        
        elif len(action_seq) > depth_limit:
            # depth limit overflow
            return None
        
        else:
            # try all possible action
            for action in puzzle.get_action_space(state):
                next_state, next_action_seq = puzzle.get_next_state(state, action), action_seq + [action]
                # if the same node is visited again in a shorter distance, it's possile to search more
                # result under the same depth limitation, therefore it should not be ignored
                if str(next_state) in state_visited and len(next_action_seq) >= state_visited[str(next_state)]:
                    continue
                state_visited[str(next_state)] = len(next_action_seq)
                res_action_seq = _dfs(next_state, next_action_seq) 
                # if found, backtrack
                if res_action_seq != None:
                    return res_action_seq

            # all tried, not found
            return None
    
    action_seq = _dfs(src_state)
    return action_seq





# template of Heuristic Search
# @h_func(state: numpy.ndarray) -> Number: should return the heuristic estimation value of state
# if solution is found, return the solution's action sequence
# if not found, return None 
def _heuristic_search(src_state, h_func):
    '''
    f(x) = g(x) + h(x)
    g(x): present cost, i.e., depth of search
    h(x): future estimated cost, given by heuristic function
    f(x): comprehensive estimated cost
    '''
    state_visited, _state_heap = {}, []

    # function closure
    # pop the node (state, action_seq, g_val, h_val) with largest f_val from heap
    def pop_heap():
        nonlocal state_visited, _state_heap
        f_val, state_str = heapq.heappop(_state_heap)
        if state_str in state_visited:
            state, action_seq, g_val, h_val = state_visited[state_str]
            return state, action_seq, g_val, h_val
        else:
            return None, None, None, None
        
    # push the node (state, action_seq, g_val, h_val) into heap (and map)
    def push_heap(state, action_seq, g_val, h_val):
        nonlocal state_visited, _state_heap
        state_visited[str(state)] = [
            np.copy(state), # state, copied
            action_seq,     # action_seq
            g_val,          # g_val
            h_val           # h_val 
        ]
        heapq.heappush(_state_heap, [g_val + h_val, str(state)])
        
        
    # use A* algorithm
    # always take the node with largest f_val as the next search node
    push_heap(state=src_state, action_seq=[], g_val=0, h_val=h_func(src_state))
    while _state_heap != []:
        state, action_seq, g_val, h_val = pop_heap()
        if puzzle.is_equal(state, puzzle.tgt_state):
            # found
            return action_seq
        
        # not found, continue to explore
        for action in puzzle.get_action_space(state):
            next_state, next_action_seq = puzzle.get_next_state(state, action), action_seq + [action]
            next_g_val, next_h_val = g_val + 1, h_func(next_state)
            if str(next_state) in state_visited:
                continue
            push_heap(next_state, next_action_seq, next_g_val, next_h_val)
        
    # not found
    return None

def get_manhattan_dist(state):
    pos_src = np.argwhere(state == 0)
    pos_tgt = np.argwhere(puzzle.tgt_state == 0)
    res = np.abs(pos_src - pos_tgt).sum()
    return res


# Heuristic Search 1: take the count of incorrect digits as heuristic function
# if solution is found, return the solution's action sequence
# if not found, return None 
def heuristic_search_1(src_state):
    # heuristic function
    # return the total count of incorrect digits (disclude vacancy)
    def get_incorrect_count(state):
        res = (state != puzzle.tgt_state).sum()
        res -= (np.argwhere(state == 0) != np.argwhere(puzzle.tgt_state == 0)).any()
        return res

    return _heuristic_search(src_state, h_func=get_incorrect_count)
    
# Heuristic Search 1: take the manhattan distance for vacancy as heuristic function
# if solution is found, return the solution's action sequence
# if not found, return None 
def heuristic_search_2(src_state):
    # heruistic function
    # return the manhattan distance for vacancy
    # between the present position and the expected potision
    def get_manhattan_dist(state):
        pos_src = np.argwhere(state == 0)
        pos_tgt = np.argwhere(puzzle.tgt_state == 0)
        res = np.abs(pos_src - pos_tgt).sum()
        return res

    return _heuristic_search(src_state, get_manhattan_dist)


if __name__ == '__main__':
    algo_list = [bfs, heuristic_search_1, heuristic_search_2]

    for algo in algo_list:
        state = puzzle.get_random_state(5)

        action_seq = algo(state)
        if action_seq != None: 
            print('algorithm succeed')
        else: 
            print('algorithm failed')

