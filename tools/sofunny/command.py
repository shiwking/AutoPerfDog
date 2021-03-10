# -*- encoding=utf8 -*-
# @Author: Anil
from poco.utils.simplerpc.utils import sync_wrapper
class Command:
    def __init__(self, client):
        super(Command, self).__init__()
        self.client = client

    def command(self, cmd, type):
        return self.call(cmd,type)
        
    @sync_wrapper
    def call(self, cmd, type):
        return self.client.call(cmd,type)