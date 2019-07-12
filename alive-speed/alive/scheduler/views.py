from django.shortcuts import render
from django.http import HttpResponse
# import the json
from django.http import JsonResponse

# import the logging, time ,datetime library
import logging, time, datetime

# import 定时框架 apscheduler，比较Celery、schedule框架
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

#import系统调用
import os
import psutil
import functools

#import http请求
import requests

#import 异步框架 asyncio,比较ThreadPoolExecutor、ProcessPoolExecutor
import asyncio

#打印系统信息
def show_info(text):
   pid = os.getpid()
   p = psutil.Process(pid)

   print('show my text: %s' % text)
   #进程ID
   print('Process id : %d' % pid)
   print('Process name : %s' % p.name())
   print('Process status : %s' % p.status())
   #打开进程socket的namedutples列表
   print(p.connections())
   #此进程的线程数
   print('Process number of threads : %s' % p.num_threads())
   #进程运行时间
   print('Process creation time : %s' % datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M:%S"))
   #当前时间
   print('now time : %s' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
   #分割线
   print('======================================================')
   return

#同步任务
def my_job(counter):
   
   show_info('in threads')
   return

#同步请求任务
def my_job2(counter):
   
   for num in range(0, 5):
      resp = requests.request("get", "http://www.baidu.com")
      print(str(resp.text))
      show_info('in thread task')
   
   show_info('in main task')
   return

#异步请求任务
def my_job3(counter):
   
   for num in range(0, 5):
      resp = requests.request("get", "http://www.baidu.com")
      print(str(resp.text))
      show_info('in thread task')
   
   show_info('in main task')
   return

#http同步请求
def my_job4():

   loop = asyncio.get_event_loop()
   tasks = [my_request(1),my_request(2),my_request(3),my_request(4),my_request(5)]
   loop.run_untill_complete(asyncio.wait(tasks))
   loop.close()

   return

async def my_request(num):

   show_info('in thread: %s' % num)
   future = asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.get, 'http://www.baidu.com'))
    
   response = await future
   

# APScheduler BlockingScheduler 阻塞式
# 同时输入http://127.0.0.1:8000/scheduler/blocking?a=2和
# http://127.0.0.1:8000/scheduler/blocking?a=1,观察后台日志的表现
# interval、date定时调度（作业只会执行一次）、cron定时调度（某一定时时刻执行）
def blocking(request):

   scheduler = BlockingScheduler()
   scheduler.add_job(my_job, 'interval', seconds=5, args=[request.GET.get("a")])
   scheduler.start()

   response = JsonResponse({'errCode': '0'})
   return response


# APScheduler backgroundScheduler 非阻塞式
def background(request):

   scheduler = BackgroundScheduler()
   scheduler.add_job(my_job, 'interval', seconds=5, args=[request.GET.get("a")])
   scheduler.start()

   response = JsonResponse({'errCode': '0'})
   return response

#子任务非阻塞，http同步阻塞
def async_with_block(request):

   scheduler = BackgroundScheduler()
   scheduler.add_job(my_job2, 'interval', seconds=5, args=[request.GET.get("a")])
   scheduler.start()

   response = JsonResponse({'errCode': '0'})
   return response

def async_no_block(request):

   scheduler = BackgroundScheduler()
   scheduler.add_job(my_job4, 'interval', seconds=5, args=[request.GET.get("a")])
   scheduler.start()

   response = JsonResponse({'errCode': '0'})
   return response

 