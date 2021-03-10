# -*- encoding=utf8 -*-
# @Author: Anil
import json
from airtest.core.api import *
from tools.sofunny.base_module import BaseModule
import time


class AutoBattlePerf(BaseModule):

    # 下载战报
    def loadWarReport(self, **my_args):
        jsonStr = json.dumps(my_args)
        return self.command("loadWarReport", jsonStr)

    # 战报下载状态
    def isLoadWarReport(self):
        return self.command("isLoadWarReport", self.getModuleName())

    # 播放战报
    def playReport(self, **w):
        jsonStr = json.dumps(w)
        return self.command("playReport", jsonStr)

    # 战报是否结束
    def isEndReport(self):
        return self.command("isEndReport", self.getModuleName())

    # 开始记录性能数据
    def startRecord(self):
        return self.command("startRecord", self.getModuleName())

    # 显示性能界面=
    def showWarProfilerMap(self):
        return self.command("showWarProfilerMap", self.getModuleName())

    # 获得性能数据
    def getWarProfilerInfo(self):
        return self.command("getWarProfilerInfo", self.getModuleName())

    # 获取当前战报播放帧数
    def getReportCurFrame(self):
        return self.command("getReportCurFrame",self.getModuleName())


if __name__ == '__main__':
    from tools.sofunny.command import Command
    from poco.drivers.unity3d import UnityPoco

    connect_device("Android://127.0.0.1:5037/" + "10.40.2.12:20078")
    poco = UnityPoco()
    poco.agent.command = Command(poco.agent.c)
    autoRunMap = AutoBattlePerf(poco.agent.command)
    autoRunMap.initModel()
    #autoRunMap.playReport(warID="27e1407c4d796607cec958141d4fa88a_1", playID=385015877, wartype=1)
    result=autoRunMap.getReportCurFrame()
    print("isend:",result)
