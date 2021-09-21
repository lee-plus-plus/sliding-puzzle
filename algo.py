import heapq
from memory_profiler import profile
from puzzle import *



# search algorithm
# ----------------

# 广度优先搜索，返回动作序列
@profile
def bfs(src_state):
    queue, state_visited = [], {}
    # 为使图搜索不重复访问节点，需要为节点构建哈希表，
    # 由于节点状态是矩阵（向量）不可哈希化，故将其转为字符串后哈希化。
    state_visited[str(src_state)] = True
    queue.append({'state': src_state, 'action_seq': []}) #存储节点
    
    while len(queue) > 0:
        now, queue = queue[0], queue[1:]
        now_state, now_action_seq = now['state'], now['action_seq']
        
        # found
        if is_equal(now_state, tgt_state):
            return now_action_seq
        
        # not found, continue to explore
        for action in get_action_space(now_state):
            next_state, next_action_seq = get_next_state(now_state, action), now_action_seq + [action]
            if str(next_state) in state_visited:
                continue
            state_visited[str(next_state)] = True
            queue.append({'state': next_state, 'action_seq': next_action_seq})  #存储节点
    
    # not found
    return None


# 深度有限搜索，返回动作序列
@profile
def dfs(src_state, depth_limit=99):
    # 由于dfs不具有最优性，为维持深度有限约束一致性，当节点以更短距离重复访问时不应被忽略
    # 令state_visited存储各节点的深度，用于比较
    state_visited = {}

    # 闭包
    # 内部递归函数
    def _dfs(state, action_seq=[]):
        nonlocal state_visited, depth_limit
        
        if is_equal(state, tgt_state):
            # found
            return action_seq
        
        elif len(action_seq) > depth_limit:
            # depth limit overflow
            return None
        
        else:
            # try all possible action
            for action in get_action_space(state):
                next_state, next_action_seq = get_next_state(state, action), action_seq + [action]
                # 若访问过，但此次以更短距离访问，有可能在有限深度内搜得更多结果，需再次进入
                if str(next_state) in state_visited and len(next_action_seq) >= state_visited[str(next_state)]:
                    continue
                state_visited[str(next_state)] = len(next_action_seq)
                res_action_seq = _dfs(next_state, next_action_seq) 
                # if found, backtrack; else, continue to the next try
                if res_action_seq != None:
                    return res_action_seq
            # not found
            return None
    
    # 调用内部递归，若未找到则返回None
    action_seq = _dfs(src_state)
    return action_seq



# 启发值函数1：不正确数码的数量(不包括空位)
def get_incorrect_count(state):
    res = (state != tgt_state).sum()
    res -= (np.argwhere(state == 0) != np.argwhere(tgt_state == 0)).any()
    return res

# 启发值函数2：空位距离正确位置的曼哈顿距离
def get_manhattan_dist(state):
    pos_src = np.argwhere(state == 0)
    pos_tgt = np.argwhere(tgt_state == 0)
    res = np.abs(pos_src - pos_tgt).sum()
    return res



# 启发式搜索
# h_func: 启发式函数
@profile
def _heuristic_search(src_state, h_func):
    # f(x) = g(x) + h(x)
    # 其中g(x)为已知前继代价（深度），h(x)为估计后继代价，由启发式函数h_func给出
    # 哈希表供查重，堆供查找最小元素，状态的字符串为堆的外键
    state_visited, _state_heap = {}, []

    # 闭包
    # 从堆中弹出最小值f_val对应的状态和动作序列
    def pop_heap():
        nonlocal state_visited, _state_heap
        f_val, state_str = heapq.heappop(_state_heap)
        if state_str in state_visited:
            state, action_seq, g_val, h_val = state_visited[state_str]
            return state, action_seq, g_val, h_val
        else:
            return None, None, None
        
    # 压入栈
    def push_heap(state, action_seq, g_val, h_val):
        nonlocal state_visited, _state_heap
        state_visited[str(state)] = [
            np.copy(state), # state
            action_seq,     # action_seq
            g_val,          # g_val
            h_val           # h_val 
        ]
        heapq.heappush(_state_heap, [g_val + h_val, str(state)])
        
        
    # use A* algorithm
    push_heap(state=src_state, action_seq=[], g_val=0, h_val=h_func(src_state))
    
    while _state_heap != []:
        state, action_seq, g_val, h_val = pop_heap()
        if is_equal(state, tgt_state):
            # found
            return action_seq
        
        # not found, continue to explore
        for action in get_action_space(state):
            next_state, next_action_seq = get_next_state(state, action), action_seq + [action]
            next_g_val, next_h_val = g_val + 1, h_func(next_state)
            if str(next_state) in state_visited:
                continue
            push_heap(next_state, next_action_seq, next_g_val, next_h_val)
        
    # not found
    return None


# 启发式搜索1：采用不正确数码的数量作为启发值函数
@profile
def heuristic_search_1(src_state):
    return _heuristic_search(src_state, get_incorrect_count)
    
# 启发式搜索2：采用空位距离正确位置的曼哈顿距离作为启发值函数
@profile
def heuristic_search_2(src_state):
    return _heuristic_search(src_state, get_manhattan_dist)
