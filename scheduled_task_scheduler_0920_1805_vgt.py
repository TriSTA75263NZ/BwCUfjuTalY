# 代码生成时间: 2025-09-20 18:05:02
from datetime import datetime
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


"""
定时任务调度器
实现定时执行任务的功能，使用PYRAMID框架和APScheduler库
"""



class SchedulerService:
    """定时任务调度器服务类"""
    def __init__(self):
        self.scheduler = BackgroundScheduler()

        # 初始化定时任务
        self.init_tasks()

    def init_tasks(self):
        """初始化定时任务"""
        # 每天凌晨1点执行task1
        self.scheduler.add_job(self.task1, CronTrigger(hour=1, minute=0))

    def task1(self):
        """任务1: 打印当前时间"""
        print("Task 1 executed at: ", datetime.now())

    def start(self):
        """启动定时任务调度器"""
        self.scheduler.start()

    def shutdown(self):
        """关闭定时任务调度器"""
        self.scheduler.shutdown()



@view_config(route_name='start_scheduler', renderer='json')
def start_scheduler(request):
    "