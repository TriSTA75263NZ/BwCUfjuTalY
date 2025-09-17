# 代码生成时间: 2025-09-17 23:19:46
import os
import subprocess
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

# 定义进程管理器类
class ProcessManager:
    def __init__(self):
        self.processes = {}
    
    # 启动进程
    def start_process(self, name, command):
        if name in self.processes:
            raise ValueError(f"Process {name} already started")
        process = subprocess.Popen(command, shell=True)
        self.processes[name] = process
        return process.pid

    # 停止进程
    def stop_process(self, name):
        if name not in self.processes:
            raise ValueError(f"Process {name} not found")
        process = self.processes.pop(name)
        process.terminate()
        process.wait()

    # 列出所有进程
    def list_processes(self):
        return {name: process.pid for name, process in self.processes.items()}

# Pyramid视图函数
@view_config(route_name='start_process', request_method='POST')
def start_process_view(request):
    pm = ProcessManager()
    name = request.json.get('name')
    command = request.json.get('command')
    try:
        pid = pm.start_process(name, command)
        return Response(f"Process {name} started with PID {pid}")
    except Exception as e:
        return Response(str(e), status=500)

@view_config(route_name='stop_process', request_method='POST')
def stop_process_view(request):
    pm = ProcessManager()
    name = request.json.get('name')
    try:
        pm.stop_process(name)
        return Response(f"Process {name} stopped")
    except Exception as e:
        return Response(str(e), status=500)

@view_config(route_name='list_processes', request_method='GET')
def list_processes_view(request):
    pm = ProcessManager()
    processes = pm.list_processes()
    return Response(processes)

# Pyramid配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('start_process', '/start_process')
    config.add_route('stop_process', '/stop_process')
    config.add_route('list_processes', '/list_processes')
    config.scan()
    return config.make_wsgi_app()
