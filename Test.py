# 最小观看时长判定
min_len = 0  # 待定


# 点击判断是否观看
def click(user, video, stay_len: float): ##点赞那些
    if stay_len > min_len:  # 若观看则更新信息
        user.new_video(video, stay_len)
        video.new_user(user, stay_len)
