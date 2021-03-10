#!/bin/bash
# -*- coding: utf-8 -*-r
import os
import sys

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 当前文件所在的目录
sys.path.append(rootPath)
print(rootPath)

import docker
import time

from setup import DOCKERBASEURL, getpropath

project_path = getpropath()[0]
python_path = os.path.join(project_path, "venv_linux", "bin", "python3")


class DockerOperation(object):
    def __init__(self):
        self.client = docker.DockerClient(base_url=DOCKERBASEURL)
        self.DockerList = []

    def ImagesList(self):
        """
        获取镜像列表信息
        :return: 镜像列表集合
        """
        cls = self.client.images.list()
        return cls

    def dockerList(self):
        """
        获取容器列表信息
        :return: 容器列表集合
        """
        cls = self.client.containers.list()
        return cls

    def get_container(self, DockerID):

        cls = self.client.containers.get(DockerID)
        return cls

    def RunPerDog(self, device):
        """
        运行性能自动化容器
        :param TestApkName:
        :return:
        """

        Commd = "python3 -u " + os.path.join("/AutoPerfDog", "core", "start_main.py ") + device + " " + "start_per"
        volume = {project_path: {"bind": "/AutoPerfDog", "mode": "rw"}}
        container = self.client.containers.run('perfdog', Commd, volumes=volume, detach=True, stdin_open=True, tty=True,
                                               user='root')
        self.DockerList.append(container.short_id)
        return container.short_id

    def Runinstall(self, device):
        """
        执行游戏客户端安装操作容器
        :param apk_url:
        :return:
        """

        Commd = "python3 -u " + os.path.join("/AutoPerfDog", "core", "start_main.py ") + device + " " + "install"
        volume = {project_path: {"bind": "/AutoPerfDog", "mode": "rw"}}
        container = self.client.containers.run('perfdog', Commd, volumes=volume, detach=True, stdin_open=True, tty=True,
                                               user='root')
        self.DockerList.append(container.short_id)
        return container.short_id

    def StopOneCOntainer(self, containerid):
        """
        停止指定容器
        :param containerid:
        :return:
        """
        pass

    def StopAllContainer(self):
        """
        停止所有容器运行
        :return:
        """
        for container in self.client.containers.list():
            container.stop()

    def DeleteOneContainer(self, containerid):
        """
        删除指定容器
        :param containerid:
        :return:
        """
        pass

    def DeleteAllContainer(self):
        """
        删除所有容器
        :return:
        """
        pass

    def GetLogs(self, DockerID):
        """
        获取容器日志
        :param DockerID:
        :return:
        """
        container = self.client.containers.get(DockerID)
        return container.logs()

    def TestResultConfirmation(self):
        """Docker 进程确认，每隔30秒确认Docker 进程是否结束，最长5分钟，如未结束当异常处理"""
        i = 0
        while i < 60:
            if len(self.dockerList()) == 0:
                break
            time.sleep(5)
            i = i + 1


if __name__ == '__main__':
    DC = DockerOperation()
    DC.RunPerfDog("79fc2ab")
