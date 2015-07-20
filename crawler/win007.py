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
url_his_ml = 'http://bf.win007.com/football/hg/Over_%s.htm' # match day. e.g. 20140712


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


# 即将进行的比赛
def cur_match_list():
    url = url_ml % utils.url_timestamp()
    data = req(url)

    if data is None:
        print 'request cur_match_list error'  # raise error
        return

    ml_ptn = re.compile(r'A\[\d+\]="(.*?)"\.split')
    m = [item.split('^') for item in ml_ptn.findall(data)]
    return [{k: item[idx] for k, idx in fixed_info} for item in m]


# 历史比赛列表
def his_match_list(match_day):
    url = url_his_ml % match_day
    data = req(url)

    if data is None:
        print 'request his_match_list error'  # raise error
        return

    item_ptn = re.compile(r'<tr height[^>]+>(.*?)</tr>')
    field_ptn = re.compile(r'<td[^>]*>(.*?)</td>')

    ret = []

    for item in item_ptn.findall(data):
        m = field_ptn.findall(item)
        ret.append({
            "match_id": utils.retrieve_id(m[-1]),
            "league": m[0],
            "home": utils.drop(m[3]),
            "visiting": utils.drop(m[5]),
            "match_time": m[1],
            "is_betting": utils.is_bet(m[-1]),
            "full_score": utils.drop_font(m[4]),
            "half_score": utils.drop_font(m[6]),
            "status": m[2],
            })
    return ret
