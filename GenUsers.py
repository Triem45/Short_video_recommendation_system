# coding=utf-8
import TimeTest
import numpy as np
from GlobalVariable import testVideos
from GlobalVariable import global_obj
from collections import deque
from scipy.stats import truncnorm
total_size = 20000  # 指明要生成的用户数

def generate_random_number_with_expectation(μ=2.5, σ=1, lower_bound=0, upper_bound=6):
    """
    生成一个期望值为μ、标准差为σ，且被截断在[lower_bound, upper_bound]区间的随机数。

    参数:
    μ (float): 期望值，默认为2.5
    σ (float): 标准差，默认为1
    lower_bound (float): 截断区间的下限，默认为0
    upper_bound (float): 截断区间的上限，默认为6

    返回:
    float: 生成的随机数
    """
    a, b = (lower_bound - μ) / σ, (upper_bound - μ) / σ  # 计算标准化区间边界
    truncated_float = truncnorm.rvs(a, b, loc=μ, scale=σ)
    return int(np.round(truncated_float))
def take_uid(user):
    return user.uid


@TimeTest.Krxk_Clock
def GenUsers():
    import threading
    print('begin generate users')
    group_size = 1000
    group_num = int(total_size / group_size) + 1
    thread_list = []
    for i in range(group_num):
        t = threading.Thread(target=HelpGenUsers, args=(i * group_size, (i + 1) * group_size))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    global_obj.GlobalUserList.sort(key=take_uid, reverse=False)
    print('generate users done')


@TimeTest.Krxk_Clock
def HelpGenUsers(start_uid, end_uid):
    from User import User
    import random
    que=deque()
    for _ in range(100):
        que.append(generate_random_number_with_expectation())
    for i in range(start_uid, end_uid):
        workphase=random.randint(0, 4)
        if(workphase==0):
          job=0
        else:job=random.randint(1, 5)
        user = User(workphase, random.randint(0, 1), job, i)
        for j in range(100):
            video_id=random.randint(1, testVideos)
            user.video_list[random.randint(0, 9)].append([video_id, 1, 1])
            score = que.popleft()
            global_obj.add_videoscore(i,video_id,score)
            que.append(score)
        global_obj.add_user_to_list(user, True)
