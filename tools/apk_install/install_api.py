# -*- coding: utf-8 -*-
import os
import sys

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 当前文件所在的目录
sys.path.append(rootPath)
print(rootPath)

import platform
import requests
import urllib.parse
from tools.atx_api.atx2_api import get_device_source_info
from MyConfigParser import MyConfigParser, getvaule, setvaule
from airtest.core.api import *
from airtest.core.android.adb import ADB
from setup import getpropath

system = platform.system()
configPath = os.path.join(getpropath()[0], "tools", "apk_install", "config.ini")
res_ui_path = os.path.join(getpropath()[0], "tools", "apk_install", "res_ui")
print(configPath)
print(res_ui_path)


class Install_api(object):
    def __init__(self, device):

        self.air_adb = ADB()
        self.adb = self.air_adb.adb_path
        self.device = device
        self.device_connect_url = get_device_source_info(self.device)["device"]["source"]["remoteConnectAddress"]
        connect_device("Android://127.0.0.1:5037/" + self.device_connect_url)
        self.model = str(shell("getprop ro.product.model")).replace(" ", "_").strip("\n").strip("\r")
        self.serialno = str(shell("getprop ro.serialno")).strip("\n")

        self.main_configPath = os.path.join(getpropath()[0], "cfg", "config.ini")
        self.build_type = getvaule(self.main_configPath, "config", "build_type")
        self.package = getvaule(self.main_configPath, "active_config", self.build_type)

    def clear_phone_apk(self):
        """
        清理当前机型的默认下载目录下的所有apk文件
        :return:null
        """

        file_path = getvaule(configPath, "Down_load_path", self.model)
        os.system(self.adb + " -s " + self.device_connect_url + " shell rm "+os.path.join(file_path,"*.apk"))

    def clear_background_activities(self):
        info = os.popen(
            self.adb + " -s " + self.device_connect_url + " shell dumpsys activity activities | grep affinity")
        activitie_List = [i.strip().replace("affinity=", "") for i in info]
        skill_activitie_List = [i for i in getvaule(configPath, "main_frame_act", self.model).split(",")]
        for i in activitie_List:
            if i not in skill_activitie_List:
                print(self.adb + " -s " + self.device_connect_url + " shell pm clear " + i)
                os.system(self.adb + " -s " + self.device_connect_url + " shell pm clear " + i)
            elif i in skill_activitie_List:
                continue

        os.system(self.adb + " -s " + self.device_connect_url + " shell input keyevent HOME")
        os.system(self.adb + " -s " + self.device_connect_url + " shell input keyevent APP_SWITCH")
        tap_pos = [i for i in getvaule(configPath, "main_frame_clear_button_pos", self.model).split(",")]
        os.system(self.adb + " -s " + self.device_connect_url + " shell input tap " + tap_pos[0] + " " + tap_pos[1])
        os.system(self.adb + " -s " + self.device_connect_url + " shell input keyevent HOME")

    def download_apk_to_local(self):
        url = getvaule(configPath, "config", "apk_url")
        UUID = url.split("/")[-1]
        download_path = os.path.join(getpropath()[0], "res", "apk")
        file_path = os.path.join(download_path, UUID)
        r1 = requests.get(url, stream=True, verify=False)
        total_size = int(r1.headers['Content-Length'])

        # 删除所有本地apk缓存
        os.system("rm -f " + os.path.join(download_path, "*.apk"))

        # 若本地本地文件已下载过，检测大小，未下载则0
        if os.path.exists(file_path):
            temp_size = os.path.getsize(file_path)  # 本地已经下载的文件大小
        else:
            temp_size = 0

        print("已存在文件大小(未存在为0)" + str(temp_size))
        print("下载文件预计大小" + str(total_size))

        # 核心部分，这个是请求下载时，从本地文件已经下载过的后面下载
        headers = {'Range': 'bytes=%d-' % temp_size}
        # 重新请求网址，加入新的请求头的
        r = requests.get(url, stream=True, verify=False, headers=headers)

        # "ab"表示追加形式写入文件
        with open(file_path, "ab") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    temp_size += len(chunk)
                    f.write(chunk)
                    f.flush()
                    ###这是下载实现进度显示####
                    # done = int(50 * temp_size / total_size)
                    # sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    # sys.stdout.flush()
        print()  # 避免上面\r 回车符
        print("下载完毕！！！")

    def download_apk_to_phone(self):
        """
        下载客户端apk至当前机型默认下载目录下
        :return:
        """

        url = getvaule(configPath, "config", "apk_url")
        file_size = 0
        UUID = url.split("/")[-1]
        file_path = getvaule(configPath, "Down_load_path", self.model)

        shell(
            "am start -a android.intent.action.VIEW -d " + url)

        tap_info = getvaule(configPath, "input_tap", self.model).split(",")

        time.sleep(int(tap_info[2]))

        shell("input tap " + tap_info[0] + " " + tap_info[1])

        now_size = 0
        while True:
            time.sleep(8)
            info = os.popen(
                self.adb + " -s " + self.device_connect_url + " shell du -k " + file_path + UUID)
            for i in info:
                now_size = i.split('\t')[0]
            if now_size == file_size:
                print(now_size)
                print(file_size)
                print("Download apk file success")
                break
            else:
                file_size = now_size

    def install_apk_phone_cmd(self):
        """
        安装下载至设备中的apk文件
        :return:
        """
        url = getvaule(configPath, "config", "apk_url")
        UUID = url.split("/")[-1]
        file_path = getvaule(configPath, "Down_load_path", self.model)
        print(self.adb + " -s " + self.device_connect_url + " shell pm install -r -g " + file_path + UUID)
        try:
            os.system(self.adb + " -s " + self.device_connect_url + " shell pm clear " + self.package)
            os.system(self.adb + " -s " + self.device_connect_url + " shell pm uninstall " + self.package)
        except:
            pass
        os.system(self.adb + " -s " + self.device_connect_url + " shell pm install -r -g " + file_path + UUID)

    def install_apk_local_cmd(self):
        url = getvaule(configPath, "config", "apk_url")
        UUID = url.split("/")[-1]
        download_path = os.path.join(getpropath()[0], "res", "apk")
        file_path = os.path.join(download_path, UUID)
        print(self.adb + " -s " + self.device_connect_url + " install -r -g " + file_path)
        os.system(self.adb + " -s " + self.device_connect_url + " install -r -g " + file_path)

    def install_apk_phone_tap(self):

        tap_info = getvaule(configPath, "more_input_tap", self.model).split(",")
        time.sleep(int(tap_info[2]))
        shell("input tap " + tap_info[0] + " " + tap_info[1])

    def clear_apk_and_uninstall(self):
        try:
            os.system(self.adb + " -s " + self.device_connect_url + " shell pm clear " + self.package)
            os.system(self.adb + " -s " + self.device_connect_url + " shell pm uninstall " + self.package)
        except:
            pass

    def is_installed(self):
        now_time = time.time()
        while True:
            time.sleep(3)
            if time.time() - now_time < 600:
                command = self.adb + " -s {} shell pm list package".format(self.device_connect_url)
                commandresult = os.popen(command)
                for pkg in commandresult:
                    # print(pkg)
                    if "package:" + self.package in pkg:
                        print("在{}上发现已安装{}".format(self.device_connect_url, self.package))
                        return True
            elif time.time() - now_time > 600:
                print("安装超过10min,在{}上没找到包{}".format(self.device_connect_url, self.package))
                return False

    def creat_ui_xml(self):
        """
        获取手机当前界面的控件信息并生成xml文件
        :return:xml文件的路径地址
        """

        file_path = getvaule(configPath, "Down_load_path", self.model)
        os.system(self.adb + " -s " + self.device_connect_url + " shell uiautomator dump " + file_path + "ui.xml")
        if not os.path.exists(os.path.join(res_ui_path, self.serialno)):
            os.makedirs(os.path.join(res_ui_path, self.serialno))

        os.system(
            self.adb + " -s " + self.device_connect_url + " pull " + file_path + "ui.xml " + os.path.join(res_ui_path,
                                                                                                          self.serialno))
        return os.path.join(res_ui_path, self.serialno, "ui.xml")

    def decode_ui_xml(self, xml_path):
        """
        用于解析Uiautomator根据安卓手机控件生成的xm文件
        :return: 控件信息集
        """
        import xml.etree.cElementTree as ET
        tree = ET.ElementTree(xml_path)
        root = tree.getroot()
        print("this" + root)


if __name__ == '__main__':
    ia = Install_api("HLRDU19702031001")
    ia.download_apk_to_local()
