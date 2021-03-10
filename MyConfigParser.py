# coding=utf-8
import configparser
import os


class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def getvaule(config_path, config_name, config_key):
    con = MyConfigParser()
    con.read(config_path)
    result = con.get(config_name, config_key)
    return result


def setvaule(config_path, config_name, config_key, config_value):
    con = MyConfigParser()
    if config_key != "" and config_value != "":
        con.read(config_path)
        con.set(config_name, config_key, config_value)
        con.write(open(config_path, "w"))
    else:
        print("config_key or config_value con not be null")
