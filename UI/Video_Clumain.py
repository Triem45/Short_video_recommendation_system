# coding=utf-8
import os.path
import pandas as pd
import sys
sys.path.append(r'C:\Users\27879\Desktop\SVRemmendation')
import scipy.sparse as sps
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "."))  # 配置项目路径变量
import IO
import time
from ReadUsers import ReadUsers,user_data,user_category_score,user_video_feature
from GlobalVariable import global_obj
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from joblib import parallel_backend
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
if __name__ == '__main__':
    # 准备工作，启动线程
    t1 = time.time()
    import threading

    th1 = threading.Thread(target=IO.ReadFromFile, args=())
    th2 = threading.Thread(target=ReadUsers, args=())
    th1.start()
    th1.join()
    th2.start()
    th2.join()

    user_records = [
        (user['work_phase'], user['gender'],user['job'])
        for user in user_data
    ]
    for video in IO.video_feature_data:
        user_work_phase= [0] * 5
        user_job=[0]*6
        avg_gender=0
        for user in IO.video_user_list[int(video['video_id'])]:
            user_work_phase[int(user_records[int(user)][0])]+=1
            user_job[int(user_records[int(user)][2])]+=1      
            avg_gender+=int(user_records[int(user)][1])
        avg_gender/=len(IO.video_user_list[int(video['video_id'])])
        additional_data = {
        'work_phase':user_work_phase,  
        'job':user_job,
        'avg_gender': avg_gender
        }
        video.update(additional_data)
    df_video_data = pd.DataFrame(IO.video_feature_data)
    video_cluster_data = []
    encoder = OneHotEncoder(handle_unknown='ignore')
    categories_encoded = encoder.fit_transform(df_video_data[['category']]).toarray()

    # 初始化标准化器
    scaler = StandardScaler()

    # 定义全局特征权重(因为直接对category加权比较困难，所以将其他所有特征设置占80%的权重，然后再各自加权)
    global_weights = {'work_phase':0.4, 'job': 0.4, 'length': 0.4, 'hot': 0.4, 'user_avgscore': 2, 'avg_gender': 0.4}
    video_ids = [] 
    # 遍历视频数据
    for i, video in enumerate(IO.video_feature_data):
        # 对特定索引的工作阶段和职业进行加权
        weighted_work_phase = np.copy(video['work_phase'])
        weighted_work_phase[0] *= 0.75
        weighted_job = np.copy(video['job'])
        weighted_job[0] *= 0.75
        
        # 合并加权后的特征与其他数值型特征
        numeric_features = np.concatenate((weighted_work_phase, weighted_job, 
                                        [video['length'], video['hot'], video['user_avgscore'], video['avg_gender']]))
        
        # 对所有特征进行归一化处理
        numeric_features_normalized = scaler.fit_transform(numeric_features.reshape(1, -1))[0]
        
        # 应用全局特征权重
        feature_weights = np.repeat(global_weights['work_phase'], len(weighted_work_phase))
        feature_weights = np.concatenate((feature_weights, 
                                        np.repeat(global_weights['job'], len(weighted_job)),
                                        [global_weights.get('length'), global_weights.get('hot'), 
                                        global_weights.get('user_avgscore'), global_weights.get('avg_gender')]))
        
        # 应用全局权重后再次调整特征
        weighted_numeric_features = numeric_features_normalized * feature_weights
        
        video_id_value = df_video_data.loc[i, 'video_id']
        video_id = video['video_id']
        video_ids.append(video_id)
        # 将video_id转换为numpy数组并reshape，再与其他特征拼接
        features_row = np.concatenate(([video_id_value],  # 注意这里是直接取值后转换为数组
                                    weighted_numeric_features,
                                    categories_encoded[i]))
        video_cluster_data.append(features_row)
    video_clu_features = np.delete(video_cluster_data, 0, axis=1) if isinstance(video_cluster_data[0], np.ndarray) else video_cluster_data[:, 1:]
'''
    # 定义要尝试的K值范围
    k_values = range(7, 15, 1)

    # 存储不同K值下的SSE和轮廓系数
    sse_values = []
    silhouette_values = []

    for k in k_values:
        with parallel_backend('loky'):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(video_clu_features)

            # 计算SSE
            sse = kmeans.inertia_
            sse_values.append(sse)

            # 计算轮廓系数
            silhouette_avg = silhouette_score(video_clu_features, kmeans.labels_)
            silhouette_values.append(silhouette_avg)

    # 绘制SSE vs. K值曲线
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, sse_values, marker='o')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.title('Elbow Method')
    plt.grid(True)
    plt.show()

    # 绘制轮廓系数 vs. K值曲线
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, silhouette_values, marker='o')
    plt.xlabel('Number of Clusters (K)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Analysis')
    plt.grid(True)
    plt.show()
'''
# 使用最佳K值重新运行K-means聚类（这里最佳K值为10）
    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(video_clu_features)

    # 获取每个用户的聚类标签
    user_cluster_labels = kmeans.labels_

    # 将聚类标签添加回原始数据集，以便进一步分析或应用
    print("聚类中心:")
    print(kmeans.cluster_centers_)
    # 创建一个包含用户ID和聚类标签的DataFrame
    user_cluster_data = pd.DataFrame({
        'video_id': video_ids,
        'cluster_label': user_cluster_labels
    })

    # 将 DataFrame 保存到 CSV 文件
    user_cluster_data.to_csv('video_cluster_assignments.csv', index=False)