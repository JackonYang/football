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

url_Europe = 'http://1x2.nowscore.com/%s.js'  # match_id 欧盘
url_Asian = 'http://vip.win007.com/AsianOdds_n.aspx?id=%s'  # match_id 亚盘


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


# 即将进行的比赛列表
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


# 欧赔 赔率历史记录与变化时间
def europe(match_id):
    """{company_id: [history list]}"""
    url = url_Europe % match_id
    data = req(url, 'utf8')

    if data is None:
        print 'request europe %s error' % match_id  # raise error
        return

    idx_start = data.find('game=Array')  # brief info
    idx_pause = data.find('var gameDetail')  # var gameDetail line

    match_brief = data[idx_start: idx_pause]  # company id
    match_detail = data[idx_pause:]  # history data of a company

    brief_ptn = re.compile(r'"(.+?)"')
    detail_ptn = re.compile(r'"(?:(\d+)\^(.+?))"')

    companys = {info[1]: info[2] for info in \
            [c.split('|') for c in brief_ptn.findall(match_brief)]}

    return {
        companys[company_id]: [item.split('|') for item in history.split(';') if item] \
            for company_id, history in detail_ptn.findall(match_detail)
        }


# 亚盘 赔率历史记录与变化时间
def asian(match_id):
    url = url_Asian % match_id
    data = req(url)

    if data is None:
        print 'request Asian %s error' % match_id  # raise error
        return

    item_ptn = re.compile(r'<tr bgcolor[^>]+>(.*?)\<\/tr\>', re.DOTALL)
    field_ptn = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL)

    ret = dict()

    for item in item_ptn.findall(data):
        m = field_ptn.findall(item)
        if m[0] and ''.join(m[2:11]):
            ret[utils.drop_img(m[0])] = [m[2:5], m[8:11], m[5:8]]
    return ret
