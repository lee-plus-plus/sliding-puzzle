import time
import os
from puzzle import *
from algo import *

if __name__ == '__main__':
    while True:
        print()
        print('%dx%d数码问题' % (width, width))
        print('请选择功能')
        print('[-1]: 退出')
        print('[ 0]: 广度优先搜索')
        print('[ 1]: 深度有限搜索')
        print('[ 2]: 启发式搜索1')
        print('[ 3]: 启发式搜索2')
        print('[ 4]: 对比实验')
        print('[ 5]: 更改拼图大小')
        print()
        selection = input('>> ')
        
        if selection == '-1':
            # 退出
            print('退出')
            break
        
        if selection == '5':
            print('请输入新的拼图大小(2~9)')
            new_width = int(input('>> '))
            if 2 <= new_width <= 9:
                reset_width(new_width)
                print('已设置为%dx%d' % (width, width))
            continue

        # 输入打乱次数
        while True:
            print('请输入打乱次数(0~50)')
            shuffle_step = int(input('>> '))
            if 0 <= shuffle_step <= 50:
                break
        # 获得初始状态
        src_state = get_random_state(shuffle_step)
        print('initial state:')
        print_state(src_state)
        print()

        # 搜索求解
        if selection == '0':
            # 广度优先搜索
            print('广度优先搜索...')
            action_seq = bfs(src_state)
            
        elif selection == '1':
            # 深度有限搜索
            print('深度有限搜索...')
            action_seq = dfs(src_state, depth_limit=shuffle_step)
        
        elif selection == '2':
            # 启发式搜索1
            print('启发式搜索1...')
            action_seq = heuristic_search_1(src_state)

        elif selection == '3':
            # 启发式搜索2
            print('启发式搜索2...')
            action_seq = heuristic_search_2(src_state)
        
        elif selection == '4':
            # 对比试验
            print('对比试验...')
            action_seq = [0, 0, 0, 0]
            timesteps = [0, 0, 0, 0, 0]
            
            print('广度优先搜索...')
            timesteps[0] = time.time()
            action_seq[0] = bfs(src_state)
            
            print('深度有限搜索...')
            timesteps[1] = time.time()
            action_seq[1] = dfs(src_state, depth_limit=shuffle_step)
            
            print('启发式搜索1...')
            timesteps[2] = time.time()
            action_seq[2] = heuristic_search_1(src_state)
            
            print('启发式搜索2...')
            timesteps[3] = time.time()
            action_seq[3] = heuristic_search_2(src_state)
            
            print('搜索完成')
            timesteps[4] = time.time()
            
            time_cost = [timesteps[i+1] - timesteps[i] for i in range(4)]
            search_name = ['广度优先搜索', '深度有限搜索', '启发式搜索1', '启发式搜索2']
            print('\t\t\t{:10}\t{:10}'.format('时间/s', '动作长度'))
            for i in range(4):
                print('{:15}\t{:2f}\t{:2d}'.format(search_name[i], time_cost[i], len(action_seq[i])))
            print()
            
            print('按任意键继续')
            input('>> ')
            os.system("clear")
            
            continue
        
        else:
            # 那也给你来个启发式搜索吧
            print('瞎搜索...')
            action_seq = heuristic_search_1(src_state)

        # 求解完毕，输出结果
        if action_seq == None:
            # solution not found
            print('solution not found. ')
        else:
            # solution found
            print('solved in %d steps. ' % len(action_seq))
            print()
            print('[ 0]: 跳过')
            print('[ 1]: 查看动画演示')
            print('[ 2]: 查看静态演示')
            print()
            selection2 = input('>> ')   
            if selection2 == '0':
                # 跳过
                pass
            elif selection2 == '1':
                # 查看动画演示
                state = np.copy(src_state)
                
                for action in action_seq:
                    os.system("clear")
                    state = get_next_state(state, action)
                    print(action)
                    print_state(state)
                    print()
                    time.sleep(1)
                    
            else:
                # 查看静态演示
                # 那也给你来个静态演示吧
                state = np.copy(src_state)
                for action in action_seq:
                    state = get_next_state(state, action)
                    print(action)
                    print_state(state)
                    print()

        # 结果输出完毕，暂停
        print('按任意键继续')
        input('>> ')
        os.system("clear")
