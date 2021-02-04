#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import subprocess
import tempfile
from testing_runner.utils import loader

# 拿到当前环境的python3目录
EXEC = sys.executable

if 'uwsgi' in EXEC:
    EXEC = '/usr/bin/python3'


class DebugCode(object):

    def __init__(self, code):
        self.__code = code
        self.resp = None
        # 创建一个临时文件
        self.temp = tempfile.mkdtemp(prefix='TestingRunner')

    def run(self):
        """ dumps debugtalk.py and run
        """
        try:
            file_path = os.path.join(self.temp, 'debugtalk.py')
            loader.FileLoader.dump_python_file(file_path, self.__code)
            # 创建一个子进程并返回子进程标准输出的输出结果，stderr=subprocess.STDOUT 把错误输出重定向到PIPE对应的标准输出
            self.resp = decode(subprocess.check_output([EXEC, file_path], stderr=subprocess.STDOUT, timeout=60))

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = 'RunnerTimeOut'

        shutil.rmtree(self.temp)


def decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')
