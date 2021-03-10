# -*- coding: utf-8 -*-
import os
import sys

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 当前文件所在的目录
sys.path.append(rootPath)
print(rootPath)

from setup import getpropath
from tools.apk_install.install_api import Install_api
from MyConfigParser import MyConfigParser, getvaule, setvaule

config_path = os.path.join(getpropath()[0], "tools", "apk_install", "config.ini")


class Install_apk(object):
    def __init__(self, device):
        self.device = device
        self.install_act = Install_api(self.device)
        self.model = self.install_act.model
        self.phone_install = True if getvaule(config_path, "phone_install", self.model) == "1" else False
        self.command_install = True if getvaule(config_path, "command_install", self.model) == "1" else False
        self.is_need_to_mv_apk = True if getvaule(config_path, "is_need_to_mv_apk", self.model) == "1" else False

    def main(self):
        if self.phone_install:
            if self.command_install:
                try:
                    self.install_act.clear_background_activities()
                    self.install_act.clear_phone_apk()
                    self.install_act.clear_apk_and_uninstall()
                    self.install_act.download_apk_to_phone()
                    self.install_act.install_apk_phone_cmd()
                    install_result = self.install_act.is_installed()
                    self.install_act.clear_background_activities()
                    print("{} install apk success:{}".format(self.device, install_result))
                except Exception as e:
                    print(e)
                    self.install_act.clear_background_activities()
                    print("{} install apk success:{}".format(self.device, False))
            else:
                try:
                    self.install_act.clear_background_activities()
                    self.install_act.clear_phone_apk()
                    self.install_act.clear_apk_and_uninstall()
                    self.install_act.download_apk_to_phone()
                    self.install_act.install_apk_phone_tap()
                    install_result = self.install_act.is_installed()
                    self.install_act.clear_background_activities()
                    print("{} install apk success:{}".format(self.device, install_result))
                except Exception as e:
                    print(e)
                    self.install_act.clear_background_activities()
                    print("{} install apk success:{}".format(self.device, False))

        else:
            try:
                self.install_act.clear_background_activities()
                self.install_act.clear_apk_and_uninstall()
                self.install_act.download_apk_to_local()
                self.install_act.install_apk_local_cmd()
                install_result = self.install_act.is_installed()
                self.install_act.clear_background_activities()
                print("{} install apk success:{}".format(self.device, install_result))
            except Exception as e:
                print(e)
                self.install_act.clear_background_activities()
                print("{} install apk success:{}".format(self.device, False))



if __name__ == '__main__':
    values = sys.argv
    device = values[1]
    install = Install_apk(device)
    install.main()
