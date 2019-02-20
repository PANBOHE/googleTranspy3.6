# -*- coding: utf-8 -*-
# @File  : pyinstall.py.py
# @Author: Panbo
# @Date  : 2019/2/20
# @Desc  :

import os
import PyInstaller
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts=['fanyi.py','-w','-F','-icon=icon.ico']
    run(opts)