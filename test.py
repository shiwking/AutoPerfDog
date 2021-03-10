
import sys
import os
# sys.path.append(r'D:\lnh.python\py project\teaching_show\blog')
print(os.path.dirname(__file__))
# 获取本文件的绝对路径  # D:/lnh.python/py project/teaching_show/blog/bin
print(os.path.dirname(os.path.dirname(__file__)))
# 获取父级目录也就是blog的绝对路径  # D:/lnh.python/py project/teaching_show/blog
rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # 当前文件所在的目录
print(rootPath)
BATH_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BATH_DIR)

