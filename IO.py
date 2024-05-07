import math
import random
import time

import pandas as pd
import TimeTest
from GlobalVariable import global_obj

file_path = r'C:\Users\27879\Desktop\SVRemmendation\Data.csv'
from PyQt5.QtCore import QObject, QThread, pyqtSignal
video_feature_data=[]
max_uid=100001
video_user_list=video_user_list = [None] * (max_uid + 1)
def take_uid(video):     ##返回视频的id号
    return video.uid


@TimeTest.time_spend_show
def ReadFromFile():
    from GenUsers import testVideos
    import threading
    thread_list = []
    data = pd.read_csv(file_path, nrows=testVideos)

    #  分成大组，简单处理，余数进1
    group_size = 2000
    group_num = int(testVideos / group_size) + 1
    for i in range(group_num):
        t = threading.Thread(target=WriteToMemory, args=(data[i * group_size:(i + 1) * group_size],))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    global_obj.GlobalVideoList.sort(key=take_uid, reverse=False)  # 升序排列


@TimeTest.time_spend_show
def WriteToMemory(data):
    from Video import Video
    for index, row in data.iterrows():
        video = Video(
            category=int(row['category']),
            uid=int(row['ID']),
            length=int(row['length']),
            name=row['name'],
            like=int(row['like']),
            comment=int(row['comment']),
            share=int(row['share']),
            watch=int(row['watch']),
        )
        if(int(video.hot<1000)):
          hot=1
        elif (int(video.hot<10000)):
          hot=2
        else:hot=3
        user_id_list = str(row['user_list']).split(';')
        user_score_list = str(row['user_score']).split(';')
        user_avgscore=0
        user_count=0
        for i,user_id in enumerate(user_id_list): 
            if(i==1):
              break
            if user_id == '':
                continue
            video.new_user(int(user_id))
            uid=int(row['ID'])
            score=user_score_list[i]
            user_avgscore+=int(score)
            user_count+=1
            global_obj.add_videoscore(user_id,uid,score)
        user_avgscore/=user_count
        global_obj.add_video_to_list(video, True)  # 采用快速模式添加
        category=int(row['category'])
        video_feature_data.append({'video_id': int(video.uid), 'category':category,'length': int(video.length),'hot': hot,'user_avgscore':user_avgscore})
        video_user_list[int(video.uid)]=user_id_list

def ConvertListToStr(ul: list):
    result = str('')
    for item in ul:
        result += str(item) + ';'
    result = result[:-1]
    return result


@TimeTest.time_spend_show
def SaveToFile():
    df = pd.DataFrame(columns=['category', 'ID', 'length', 'comment', 'like', 'watch', 'share', 'name', 'user_list'])
    for i, video in enumerate(global_obj.GlobalVideoList):
        df.loc[i + 2] = [video.category, video.uid, video.length, video.comment, video.like, video.watch,
                         video.share, video.name, ConvertListToStr(video.user_list)]
    print("Saving")
    df.to_csv(file_path + '.bak', encoding='utf-8', index=False)

