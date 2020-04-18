#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import requests
import time


# 发送短信验证
def send_verify_code(telephone):
    # 这里使用的是网易云信提供的接口，根据平台开发者文档进行参数配置
    url = "https://api.netease.im/sms/sendcode.action"
    # 使用new()创建指定加密模式的hash对象
    # 加密当前时间戳生成16进制随机数（sha512生成的加密hash转换成的16进制字符长度为是128）
    nonce = hashlib.new("sha512", str(time.time()).encode('utf-8')).hexdigest()
    # 获取当前UTC时间戳
    curtime = str(int(time.time()))
    # 校验值checksum
    sha1 = hashlib.sha1()
    secret = "559ecf63ec7c"
    sha1.update((secret + nonce + curtime).encode('utf-8'))
    check_sum = sha1.hexdigest()
    headers = {
        "AppKey": "d91268a309b52abd451095e48bda6628",  # 开发者平台分配的appkey
        "Nonce": nonce,  # 随机数（最大长度128个字符）
        "CurTime": curtime,  # 当前UTC时间戳
        "CheckSum": check_sum
    }
    post_data = {
        "mobile": telephone
    }
    # 使用第三方請求庫requests来发送请求
    response = requests.post(url, data=post_data, headers=headers)
    return response
