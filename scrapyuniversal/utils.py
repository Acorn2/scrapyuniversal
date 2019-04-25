#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/21 20:34
software: PyCharm
description: 
'''
from os.path import realpath, dirname
import json


def get_config(name):
    '''
    读取configs目录下的json文件，其中主要是Spider内的属性，返回具体配置信息.
    :param name:json文件名
    :return:
    '''
    config_path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(config_path, 'r', encoding='utf-8') as fr:
        return json.loads(fr.read())
