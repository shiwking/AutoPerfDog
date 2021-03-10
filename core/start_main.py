#!/bin/bash
# -*- coding: utf-8 -*-
import os
import sys

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 当前文件所在的目录
sys.path.append(rootPath)
print(rootPath)

import platform

system = platform.system()
from setup import getpropath

project_path = getpropath()[0]

def main():
    values = sys.argv
    device = values[1]
    action = values[2]
    if action == "install":
        os.system("python3 -u " + os.path.join(project_path, "core", "install_main.py ") + device)
    elif action == "start_per":
        os.system("chmod 777 -R " + os.path.join(getpropath()[0]))
        os.system("python3 -u " + os.path.join(project_path, "core", "PerfServiceMain.py ") + device)
    else:
        print("action failed")


if __name__ == '__main__':
    main()
