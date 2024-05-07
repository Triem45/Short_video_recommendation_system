# coding=utf-8
import math
import TimeTest
import numpy as np
import pandas as pd
from GlobalVariable import testVideos
from GlobalVariable import global_obj
from collections import deque
from scipy.stats import truncnorm
from IO import video_feature_data
total_size = 20000  # 指明要生成的用户数
file_path = r'C:\Users\27879\Desktop\SVRemmendation\UserData.csv'
user_data=[]
user_category_score={}
user_video_feature=[]
# 初始化两个空列表来分别存储 length 和 hot 数据
def take_uid(user):
    return user.uid
@TimeTest.time_spend_show
def ReadUsers():
    import threading
    thread_list = []
    data = pd.read_csv(file_path, nrows=testVideos)

    #  分成大组，简单处理，余数进1
    group_size = 2000
    group_num = int(testVideos / group_size) + 1
    for i in range(group_num):
        t = threading.Thread(target=HelpReadUsers, args=(data[i * group_size:(i + 1) * group_size],))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    global_obj.GlobalVideoList.sort(key=take_uid, reverse=False)  # 升序排列


@TimeTest.time_spend_show
def HelpReadUsers(data):
    from User import User
    for index, row in data.iterrows():
        user = User(
            work_phase = int(row['work_phase']),
            gender = int(row['gender']),
            job = int(row['job']),
            uid=int(row['UID']),
        )
        user_data.append({'user_id': user.uid, 'work_phase': user.work_phase,'gender': user.gender,'job':user.job})
        user_category_score[user.uid] = {}
        video_list = str(row['video_list']).split(';')
        video_data_array = []
        # 遍历每个视频数据字符串
        for video_data_str in video_list:
        # 使用 split(',') 分割单个视频数据字符串，得到包含视频ID和得分的元组
            video_data = video_data_str.split(',')
        # 确保数据有效（例如，每个视频数据都有且仅有三个部分）
            if len(video_data) == 3:
            # 将元组添加到二维数组中
               video_data_array.append([video_data[0],video_data[1], video_data[2]])
        for i,video_data in enumerate(video_data_array): 
            if video_data[1] == '': 
                continue
            lencount=i
            score=int(video_data[2])
            uid=int(row['UID'])
            global_obj.add_videoscore(uid,video_data[1],score)
            #创建记录用户看过的每一类视频总数的数组
            count_arr = np.ones(10, dtype=int)
            
            category=int(video_data_array[i][0])
            if category in user_category_score[user.uid]:
                user_category_score[user.uid][category] = (user_category_score[user.uid][category]*count_arr[category]+score)/(count_arr[category]+1)
                count_arr[category]+=1
            else:
                user_category_score[user.uid][category] = score
        
        global_obj.add_user_to_list(user, True)  # 采用快速模式添加

