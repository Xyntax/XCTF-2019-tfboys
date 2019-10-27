# !/usr/bin/env python
#  -*- coding: utf-8 -*-
import requests
import time
import urllib2
import json

IPs = """
47.105.117.64
47.104.200.183
114.215.124.80
47.104.215.190
47.105.88.64
115.28.208.149
120.27.24.89
115.28.209.119
114.215.125.146
47.105.82.54
115.29.148.67
115.28.209.8
115.29.140.95
120.27.24.55
115.28.208.217
118.190.155.203
115.28.131.155
115.28.208.33
47.105.124.40
47.104.216.84
47.105.89.28
47.104.139.36
"""

error_token = '43d8c7c51fea53a94bd5335b5fc3c677404b01041029d86048dc360cdef54363'
info_token = '3d86cfd080ffd60f5f812c9ffb1d1dfc06ddae2bc7b43e746bc592e9200469aa'


def send_msg(msg, token):
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
    post_data = {
        'msgtype': 'text',
        'text': {"content": msg}
    }
    req = urllib2.Request(webhook, json.dumps(post_data), headers={'Content-Type': 'application/json'})
    try:
        urllib2.urlopen(req).read()
    except Exception, e:
        pass


ip_list = IPs.strip().split('\n')
while True:
    for ip in ip_list:
        try:
            r = requests.get('http://' + ip + ':5679', timeout=3)
            if 'have fun' not in r.content:
                send_msg(ip, error_token)
            # if '/home/ubuntu/web3/model/upload' in r.content:
            #     send_msg('upload success: ' + ip, info_token)
            else:
                print 'pass:', ip
        except Exception, e:
            send_msg(ip + str(e), error_token)
    time.sleep(10)

