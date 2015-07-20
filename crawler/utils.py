# -*- Encoding: utf-8 -*-
import time
import re


def url_timestamp():
    return int(time.time()) * 1000


_span_prog = re.compile(r'\s*<span[^>]*>(.*?)</span>\s*')
def drop_span(content):
    return _span_prog.sub('', content)


_font_prog = re.compile(r'<font [^>]+?>([^<]*?)</font>')
def drop_font(content):
    return _font_prog.sub(r'\1', content)


_img_prog = re.compile(r'\s*<img [^>]+>\s*')
def drop_img(content):
    return _img_prog.sub('', content)


def drop(content):
    return drop_img(drop_span(content))


_matchid_prog = re.compile(r'analysis\((\d+)\)')
def retrieve_id(content):
    m = _matchid_prog.search(content)
    return m.group(1)


def is_bet(content):
    return content.find('zd.gif') > 0


headers_templates = {
    'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Referer': 'http://score1.win007.com/',
    'Connection': 'keep-alive',
}
