# -*- coding: utf-8 -*-
__author__ = "yangzhouzhen"

import os
import sys

rootPath = os.getcwd()
sys.path.append(rootPath)

DOCKERBASEURL='tcp://10.30.20.29:2375'
#DOCKERBASEURL = 'tcp://10.30.20.100:2375'


def get_project_name():
    # 获取当前项目的名称
    project_name = os.path.basename((os.path.dirname(__file__)))
    return project_name


def getpropath():
    # 获取当前项目的根目录路径
    curPath = os.path.abspath(os.path.dirname(__file__))
    report_path = os.path.join(curPath, "doc")
    return curPath, report_path


if __name__ == '__main__':
    print(getpropath())
    print(get_project_name())
