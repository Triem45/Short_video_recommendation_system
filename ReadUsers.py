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
file_path = r'D:\SVRemmendation\UserData.csv'
user_data=[]
user_category_score={}
user_video_feature=[]
# 初始化两个空列表来分别存储 length 和 hot 数据
lengths = []
hots = []




def take_uid(user):
    return user.uid

@TimeTest.Krxk_Clock
def ReadUsers():
    # 遍历原数据列表，将 length 和 hot 分别添加到对应的列表中
    for feature in video_feature_data:
        lengths.append(feature['length'])
        hots.append(feature['hot'])

    # 将长度列表和热度列表转换为numpy数组，并以video.uid作为索引
    video_lengths = np.array(lengths)
    video_hots= np.array(hots)     

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


@TimeTest.Krxk_Clock
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
        lencount=1
        lensum=0
        low_hot=0
        mid_hot=0
        high_hot=0
        for i,video_id in enumerate(video_data_array[1]): 
            if video_id == '': 
                continue
            lencount=i
            lensum+=lengths[int(video_id)]
            if(hots[int(video_id)]==1):
                low_hot+=1
            elif (hots[int(video_id)]==2):
                mid_hot+=1
            else:high_hot+=1
            user.video_list[int(video_data_array[i][0])].append([int(video_id), 1, 1])
            score=int(video_data_array[2][i])
            uid=int(row['UID'])
            global_obj.add_videoscore(uid,video_id,score)
            #创建记录用户看过的每一类视频总数的数组
            count_arr = np.ones(10, dtype=int)
            
            category=int(video_data_array[i][0])
            if category in user_category_score[user.uid]:
                user_category_score[user.uid][category] = (user_category_score[user.uid][category]*count_arr[category]+score)/(count_arr[category]+1)
                count_arr[category]+=1
            else:
                user_category_score[user.uid][category] = score
        
        user_video_feature.append({'user_id': user.uid,'avglen':math.floor(lensum/lencount), 'low_hot': low_hot, 'mid_hot': mid_hot, 'high_hot': high_hot})
        global_obj.add_user_to_list(user, True)  # 采用快速模式添加

