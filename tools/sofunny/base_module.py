# -*- encoding=utf8 -*-
# @Author: Anil
import json
class BaseModule:
		def __init__(self, command):
			self.fcommand = command

	# 获得跑地图的区块信息
		def initModel(self):
			return self.command("initModel", self.getModuleName())

		def getModuleName(self):
			moduleName = self.__class__.__name__
			print(" moduleName ",moduleName)
			return moduleName

		def command(self, cmd, type):
			jsonText = self.fcommand.call(cmd,type)
			print(jsonText)
			jsonData = json.loads(jsonText)
			print(jsonData["status"])
			return jsonData

