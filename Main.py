# -*- coding: utf-8 -*-
import os
import sys

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 当前文件所在的目录
sys.path.append(rootPath)
print(rootPath)

import platform

system = platform.system()

import sys
import tools.atx_api.atx2_api as atx
from multiprocessing import Process,Manager
from docker_core.DockerOperation_Linux import DockerOperation

from MyConfigParser import getvaule, setvaule, MyConfigParser
from setup import getpropath

install_config_path = os.path.join(getpropath()[0], "tools", "apk_install", "config.ini")
cfg_config_path = os.path.join(getpropath()[0], "cfg", "config.ini")
python3_win_path = os.path.join(getpropath()[0], "venv_windows", "bin", "python3 ")
python3_linux_path = os.path.join(getpropath()[0], "venv_linux", "bin", "python3 ")


def main():
    values = sys.argv
    apk_url = values[1]
    url_head = "http://soft.f.xmfunny.com:8888/sausage/apk"
    apk_build_type = apk_url.split("_")[0]
    url = ""
    if apk_build_type == "dev":
        url = url_head + "/开发/" + apk_url
    elif apk_build_type == "first-test":
        url = url_head + "/先行/" + apk_url

    setvaule(install_config_path, "config", "apk_url", url)
    setvaule(cfg_config_path, "config", "build_type", apk_build_type)

    atx_devices = atx.get_devices_info()["devices"]
    devices_in_config = getvaule(cfg_config_path, "config", "devices").split(",")
    devices_info = []
    for i in atx_devices:
        if i["udid"] in devices_in_config and i["owner"] == None:
            atx.add_device(i["udid"])
            devices_info.append(i)
    real_devices = ""
    for j in devices_info:
        real_devices = real_devices + j["udid"] + ","
    real_devices = real_devices.strip(",")
    setvaule(cfg_config_path, "config", "real_devices", real_devices)
    real_devices_list = getvaule(cfg_config_path, "config", "real_devices").split(",")

    if system == "Windows":
        pass
    elif system == "Linux":
        docker_start = DockerOperation()
        install_container_list = {}
        for device in real_devices_list:
            container_id = docker_start.Runinstall(device)
            install_container_list[device] = container_id

        p_list = []
        manager=Manager()
        perf_container_list = manager.dict()
        lock=manager.Lock()
        for k in install_container_list:
            container = docker_start.get_container(DockerID=install_container_list[k])
            p = Process(target=check_is_start_per_docker, args=(k, container, docker_start, perf_container_list,lock))
            p_list.append(p)

        for i in p_list:
            i.start()

        for i in p_list:
            i.join()


        p2_list=[]
        for c in perf_container_list:
            per_container = docker_start.get_container(DockerID=perf_container_list[c])
            p = Process(target=get_per_container_end_code, args=(c, per_container))
            p2_list.append(p)

        for i in p2_list:
            i.start()

        for i in p2_list:
            i.join()


def get_per_container_end_code(dev,container):
    try:
        info=container.wait(timeout=2400)
        StatusCode=info["StatusCode"]
        print(StatusCode)
        if StatusCode==0 or StatusCode=="0":
            print("{} get per data success,docker id {}".format(dev,container.id))
    except Exception as e:
        print(e)
        print("{} get per data failed,docker id {}".format(dev, container.id))

def check_is_start_per_docker(dev, container, docker_start,shareDict,lock):
    result = check_install_result(dev, container)
    if result == True:
        print(dev, True)
        container_id = docker_start.RunPerDog(dev)
        with lock:
            print("recording {} per_container_id".format(dev))
            shareDict[dev] = container_id
    elif result == False:
        print(dev, False)


def check_install_result(dev, container):
    info = container.attach(stdout=True, stderr=True, logs=True, stream=True)
    for i in info:
        log_line = i.decode().strip()
        # print(log_line)
        if "install apk success:" in log_line:
            if log_line.split(":")[-1] == "True":
                print(dev + " docker_install success:" + log_line.split(":")[1])
                return True
            elif log_line.split(":")[-1] == "False":
                print(dev + " docker_install success:" + log_line.split(":")[1])
                return False
    return False


if __name__ == '__main__':
    main()
