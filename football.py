# -*- Encoding: utf-8 -*-
import os
import re
import json
import codecs
import time

from httplib2 import Http
from jinja2 import Environment, PackageLoader


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

template_dir = os.path.join(BASE_DIR, "templates")
output_dir = os.path.join(BASE_DIR, "output")
ignore_filename = os.path.join(BASE_DIR, "match_ignore.ini")

headers_templates = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
    'Content-type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
}


def download(url, method='GET'):
    h = Http()
    headers = headers_templates.copy()
    rsp, content = h.request(url, method, headers=headers)
    return content

def parse_score(content, identifier):
    ptn = re.compile(r'var\s+%s_data\s*=\s*([^;]*);' % identifier)
    data_str = ptn.search(content).group(1).replace("\"", "\\\"").replace("'", "\"")
    return [(item[0], item[8] + item[9], item[2]) for item in json.loads(data_str)]

def filter_topn(orig, exclude=[], topn=6):
    # time, total score, matchtype
    return [item[1] for item in orig if item[2] not in exclude][:topn]

def calc(scores, peak=3):
    # sum6, sum3, avg6, avg3, avg
    sum_total = sum(scores)
    sum_peak = sum(scores[:peak])
    avg_total = 1.0 * sum_total / len(scores)
    avg_peak = 1.0 * sum_peak / peak
    avg = (avg_total + avg_peak) / 2
    return sum_total, sum_peak, avg_total, avg_peak, avg

def merge_list(host, guest, vs):
    return [(h, g, v) for h, g, v in zip(host, guest, vs)]


def disp(host=u'host', guest=u'guest', start_time='', **kwargs):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    env = Environment(loader=PackageLoader('football', template_dir))
    template = env.get_template('index.html')

    out_filename = os.path.join(output_dir, '%s-%s-%s.html' % (host, guest, start_time.split(' ')[0]))
    with codecs.open(out_filename, 'w', 'utf8') as f:
        f.write(template.render(**kwargs))
    print 'success! saved in %s' % os.path.abspath(out_filename)

def read_ignore():
    matches = []
    try:
        with codecs.open(ignore_filename, 'r', 'utf8') as f:
            matches = [line.strip() for line in f.readlines()]
    except:
        pass
    return matches


def brief(text):
    prog = re.compile(ur'<meta name="keywords" content="([^,]*) VS ([^,]*),')
    m = prog.search(text)

    t_prog = re.compile(ur"var strTime='([^;]*)';")
    t = t_prog.search(text)
    return m.group(1).decode('utf8'), m.group(2).decode('utf8'), t.group(1)


def main(url):
    content = dict()

    content['url'] = url
    content['topn'] = 6
    content['exclude_match'] = read_ignore()

    c = download(content['url'])

    if c is None:
        print 'error! contact: jiekunyang@gmail.com'
        return None

    content['host'], content['guest'], content['start_time'] = brief(c)

    content['orig_host'] = parse_score(c, 'h')
    content['orig_guest'] = parse_score(c, 'a')
    content['orig_vs'] = parse_score(c, 'v')

    topn_host = filter_topn(content['orig_host'], content['exclude_match'], content['topn'])
    topn_guest = filter_topn(content['orig_guest'], content['exclude_match'], content['topn'])
    topn_vs = filter_topn(content['orig_vs'], content['exclude_match'], content['topn'])

    content['topn_host'] = topn_host
    content['topn_guest'] = topn_guest
    content['topn_vs'] = topn_vs
    content['vs_num'] = len(topn_vs)

    calc_host = calc(topn_host)
    calc_guest = calc(topn_guest)
    calc_vs = calc(topn_vs)

    content['result'] = merge_list(calc_host, calc_guest, calc_vs)
    content['result_col_name'] = [u'6场和', u'3场和', u'6场平均', u'3场平均', u'6进3平均']
    content['avg_total'] = (calc_host[-1] + calc_guest[-1] + calc_vs[-1]) / 3.0
    content['avg_hg'] = (calc_host[-1] + calc_guest[-1]) / 2.0

    disp(**content)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = raw_input(u'url: ')
    main(url)
