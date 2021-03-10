# -*- coding: utf-8 -*-r

import docker
import os
from setup import *

from time import sleep

class DockerOperation(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url=DOCKERBASEURL)
        self.DockerList=[]

    def ImagesList(self):
        """获取镜像列表"""
        cls=self.client.images.list()
        return cls

    def dockerList(self):
        """获取容器运行列表"""
        cls=self.client.containers.list()
        return cls

    def Runcontainers(self,JobName,DevName,JobClass=SCRIPTFILEPATH):
        """运行一个容器"""
        print("testPass")
        JobName=JobName+"  "
        DevName=DevName+"  "
        Commd="python3  run.py "+JobClass+JobName+DevName
        volume = {"/Muilt": {"bind": "/Muilt", "mode": "rw"}}
        container = self.client.containers.run('airtest',Commd,volumes=volume,detach=True)
        self.DockerList.append(container.short_id)
        return container.short_id

    def RunPerfDog(self,TestApkName):
        """运行一个容器"""
        print("测试已启动，请稍等30分钟后查看报告！")
        print("http://10.30.20.29:8888/linediagram/")
        TestApkName=TestApkName

        Commd="python3  AutoPerfMain.py "+TestApkName
        volume={"/AutoPerfDog": {"bind": "/AutoPerfDog", "mode": "rw"}}
        container = self.client.containers.run('perfdog',Commd,volumes=volume,detach=True)
        self.DockerList.append(container.short_id)
        return container.short_id

    def StopAllContainer(self):
        """停止所有容器运行"""
        for container in self.client.containers.list():
            container.stop()

    def GetLogs(self,DockerID):
        """获取容器日志"""
        container = self.client.containers.get(DockerID)
        return  container.logs()

    def TestResultConfirmation(self):
        """Docker 进程确认，每隔30秒确认Docker 进程是否结束，最长5分钟，如未结束当异常处理"""
        i=0
        while i<60:
            if len(self.dockerList())==0:
               break
            sleep(5)
            i=i+1


if __name__ == '__main__':
    import sys
    Commod=sys.argv
    TestAPKName=Commod[1]
    DC=DockerOperation()
    volume={"/AutoPerfDog": {"bind": "/AutoPerfDog", "mode": "rw"}}
    DC.RunPerfDog(TestAPKName)


