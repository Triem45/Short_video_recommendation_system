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
from ReadUsers import ReadUsers,user_category_score,user_video_feature
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

    # 创建二维数组存储用户对各类视频的平均评分
    user_category_scores_array = []
    for user_id, category_scores in user_category_score.items():
        user_scores = [category_scores.get(category, 0) for category in range(10)]  # 0到9表示所有类别
        user_category_scores_array.append(user_scores)
    user_category_scores_array = np.array(user_category_scores_array)
    # 将 user_video_feature 转换为 DataFrame
    user_df = pd.DataFrame(user_video_feature)
    user_ids = user_df ['user_id'].tolist()  # 提取 user_id 列并转换为列表
    # 提取除 user_id 之外的其他属性，并转为 NumPy 数组
    user_other_attributes = user_df[['avglen', 'low_hot', 'mid_hot', 'high_hot']].values
    weights = np.array([ 0.1, 0.05, 0.05, 0.05])
    user_other_attributes=user_other_attributes*weights
    user_features_array = np.concatenate((user_category_scores_array, user_other_attributes), axis=1)
    
    weighted_features = user_features_array
    '''
    # 定义要尝试的K值范围
    k_values = range(5, 45, 1)

    # 存储不同K值下的SSE和轮廓系数
    sse_values = []
    silhouette_values = []

    for k in k_values:
        with parallel_backend('loky'):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(weighted_features)

            # 计算SSE
            sse = kmeans.inertia_
            sse_values.append(sse)

            # 计算轮廓系数
            silhouette_avg = silhouette_score(weighted_features, kmeans.labels_)
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
    # 使用最佳K值重新运行K-means聚类（这里假设最佳K值为15，实际应根据SSE或轮廓系数曲线选择）
    kmeans = KMeans(n_clusters=11, random_state=42)
    kmeans.fit(weighted_features)

    # 获取每个用户的聚类标签
    user_cluster_labels = kmeans.labels_

    # 将聚类标签添加回原始数据集，以便进一步分析或应用
    print("聚类中心:")
    print(kmeans.cluster_centers_)
    # 创建一个包含用户ID和聚类标签的DataFrame
    user_cluster_data = pd.DataFrame({
        'user_id': user_ids,
        'cluster_label': user_cluster_labels
    })

    # 将 DataFrame 保存到 CSV 文件
    user_cluster_data.to_csv('user_cluster_assignments.csv', index=False)