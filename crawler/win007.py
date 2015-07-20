# -*- Encoding: utf-8 -*-
"""球探网爬虫
TODO:
    1. 球探网不同页面, 字符编码不同. 目前手动处理, 需改为自动.

"""
import re

import socket
from httplib2 import Http

import utils

# match list
url_ml = 'http://live.win007.com/vbsxml/bfdata.js?%s'  # timestamp


def req(url, encode='gbk', method='GET'):
    h = Http(timeout=2)
    headers = utils.headers_templates.copy()
    try:
        rsp, content = h.request(url, method, headers=headers)
    except socket.timeout:
        return None

    if rsp['status'] != '404':  # TODO; status code check
        return content.decode(encode).encode('utf8')


fixed_info = (  # match list, bf_data cols
        ("match_id", 0),
        ("league", 2),  # name of league
        ("home", 5),  # name of home team
        ("visiting", 8),  # name of visiting team
        ("match_time", 11),  # match start time
        ("is_betting", 28),
        ("notes", 30),
        )


# 当前比赛列表
def cur_match_list():
    url = url_ml % utils.url_timestamp()
    data = req(url)

    if data is None:
        print 'request cur_match_list error'  # raise error
        return

    ml_ptn = re.compile(r'A\[\d+\]="(.*?)"\.split')
    m = [item.split('^') for item in ml_ptn.findall(data)]
    return [{k: item[idx] for k, idx in fixed_info} for item in m]
