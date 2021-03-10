#!/bin/bash
# -*- coding: utf-8 -*-
import os
import sys

rootPath = os.path.dirname(__file__)  # 当前文件所在的目录
sys.path.append(rootPath)

import platform

system = platform.system()

import re
import subprocess
import time
from pprint import pprint

import requests
from logzero import logger

server_url = "http://10.40.2.12:4000"
#server_url = "http://10.30.20.29:4000"
token = "11ca19454e0d40079bc3451198b4fa68"
#token = "78b55bb0bd4a4a599e79630b6640fb4c"

def make_url(path):
    if re.match(r"^https?://", path):
        return path
    return server_url + path


def request_api(path, method="GET", **kwargs):
    kwargs['headers'] = {"Authorization": "Bearer " + token}
    r = requests.request(method, make_url(path), **kwargs)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        pprint(r.text)
        raise
    return r.json()


def get_user_info():
    r = request_api("/api/v1/user")
    return r


def get_devices_info():
    r = request_api("/api/v1/devices")#,params={"usable": "true"}
    return r


def get_device_info(udid):
    r = request_api("/api/v1/devices/" + udid)
    return r


def get_device_source_info(udid):
    r = request_api("/api/v1/user/devices/" + udid)
    return r


def add_device(udid, idleTimeout=None):
    r = request_api("/api/v1/user/devices", method="post", json={"udid": udid, "idleTimeout": idleTimeout})
    return r


def update_device_activated_time(udid):
    r = request_api("/api/v1/user/devices/%s/active" % (udid))
    return r


def delete_device(udid):
    r = request_api("/api/v1/user/devices/" + udid, method="delete")
    return r


def main():
    """
    test
    :return:
    """
    # 获取用户信息
    ret = request_api("/api/v1/user")
    logger.info("User: %s", ret['username'])

    # 获取可用设备列表
    ret = request_api("/api/v1/devices", params={"usable": "true"})
    if not ret['devices']:
        raise EnvironmentError("No devices")
    logger.info("Device count: %d", ret['count'])

    # 占用设备
    device = ret['devices'][0]
    udid = device['udid']
    logger.info("Choose device: \"%s\" udid=%s", device['properties']['name'],
                udid)
    ret = request_api("/api/v1/user/devices",
                      method="post",
                      json={"udid": udid})
    print(ret)

    try:
        # 获取占用设备信息
        ret = request_api("/api/v1/user/devices/" + udid)
        source = ret['device']['source']
        pprint(source)

        # 安装应用
        logger.info("install app")
        provider_url = source['url']
        ret = request_api(
            provider_url + "/app/install",
            method="post",
            params={"udid": udid},
            data={
                "url":
                    "https://github.com/openatx/atxserver2/releases/download/v0.2.0/ApiDemos-debug.apk"
            })
        pprint(ret)

        # 运行测试
        adb_remote_addr = source['remoteConnectAddress']
        subprocess.run(['adb', 'connect', adb_remote_addr])
        time.sleep(1)
        # d = u2.connect_usb(adb_remote_addr)
        # print(d.info)
        # d.app_start("io.appium.android.apis")
        # d.xpath("App").click()  # same as d(text="App").click()
        # logger.debug("Assert Alert button exists")
        # assert d(text="Alarm").wait()

    finally:
        # 释放设备
        ret = request_api("/api/v1/user/devices/" + udid, method="delete")
        print(ret)


if __name__ == "__main__":
    print(get_devices_info())
    # print(add_device(udid="b6719d65"))
    # print(delete_device(udid="b6719d65"))
    # main()
    pass
