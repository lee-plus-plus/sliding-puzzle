import numpy as np


# global variables
# ---------------

# 数字拼图宽度
width = 4
# 动作状态集合（上下左右）
whole_action_space = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]
# 完成状态（目标状态，即所有数字顺序排列的状态）
tgt_state = np.reshape(np.arange(width ** 2), [width, width]).astype(int)




# tool functions
# --------------

# 重设数字拼图宽度
def reset_width(new_width):
    global width, tgt_state
    width = new_width
    tgt_state = np.reshape(np.arange(width ** 2), [width, width]).astype(int)

# 提取空洞坐标
def get_hole_position(state):
    pos = np.argwhere(state == 0)[0]
    return pos

# 判断两个状态是否相等
def is_equal(state_1, state_2):
    return (state_1 == state_2).all()

# 空洞位置是否合法(是否在 width x width 内)
def is_pos_inside(pos):
    return np.all([0, 0] <= pos) and np.all(pos <= [width-1, width-1])

# 获取动作空间
def get_action_space(state):
    hole_pos = get_hole_position(state)
    action_space = [action for action in whole_action_space if is_pos_inside(hole_pos + action)]
    return np.array(action_space)

# 获取动作执行后状态(不检测动作合法性)
def get_next_state(state, action):
    pos = get_hole_position(state)
    next_pos = pos + action
    next_state = np.copy(state) # 深拷贝
    next_state[pos[0], pos[1]], next_state[next_pos[0], next_pos[1]] = next_state[next_pos[0], next_pos[1]], next_state[pos[0], pos[1]]
    return next_state

# 打印数字拼图矩阵
def print_state(state):
    for i in range(width):
        for j in range(width):
            print('%3d ' % state[i][j], end='') if state[i][j] != 0 else print('    ', end='')
        print()

# 生成一个合法的随机状态(由打乱得到)
def get_random_state(shuffle_step=width**2):
    global tgt_state
    state = np.copy(tgt_state) #深拷贝
    
    for i in range(shuffle_step):
        action_space = get_action_space(state)
        np.random.shuffle(action_space)
        action = action_space[0]
        state = get_next_state(state, action)
    return state


if __name__ == '__main__':
    # 简单的游戏demo
    state = get_random_state(shuffle_step=10)

    print()
    print('%dx%d数码问题' % (width, width))

    while not is_equal(state, tgt_state):
        action_space = get_action_space(state)

        print('当前状态')
        print_state(state)
        print('输入按键，选择可采取行动')
        for i in range(len(action_space)):
            print('[{}]: {}'.format(i, action_space[i]))

        action_idx = int(input('>> '))
        state = get_next_state(state, action_space[action_idx])

    print('当前状态')
    print_state(state)
    print('游戏完成')
