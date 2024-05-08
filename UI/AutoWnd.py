import concurrent.futures
import logging
import random
import sys
import time
sys.path.append(r'D:\SVRemmendation')
import TimeTest
from GenUsers import total_size
from GlobalVariable import refresh_frequency
from UserLoginWnd import UserLoginWndLogic
from PyQt5.QtCore import QObject, QRunnable, QThreadPool
# 设置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoWnd(UserLoginWndLogic):
    def __init__(self):
        super().__init__()

    def simulate_user(self, user_id):
        try:
            cz = random.randint(0, 1)
            if cz == 0:
                return
            self.get_in_user(user_id)

            for j in range(1, 3*refresh_frequency):###此处后面参数可以改 表示模拟多少次观看，前面权重表示多少次刷新
                ilike = random.randint(0, 4)
                if ilike > 1:
                    self.like()
                    
                icomment = random.randint(0, 4)
                if icomment > 2:
                    self.comment()
                ishare = random.randint(0, 4)
                if ishare > 3:
                    self.share()

                self.clicked_play()
        except Exception as e:
            logger.error(f"Error while simulating user {user_id}: {e}")

class AutoSimulationManager:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=50)  # 创建线程池，设置最大线程数
    @TimeTest.time_spend_show
    def start_auto_simulation(self):
        futures = []
        start_time = time.time()  # 记录开始执行任务的时间

        for i in range(10):## 模拟多少个用户的观看行为
            auto_wnd = AutoWnd()
            future = self.executor.submit(auto_wnd.simulate_user, i)
            futures.append(future)

        concurrent.futures.wait(futures)  # 等待所有任务完成

        end_time = time.time()  # 记录所有任务完成的时间
        total_runtime = end_time - start_time  # 计算线程池运行总时间（秒）

        print("线程池运行总时间：%.6f 秒" % total_runtime)

        print("over")