# -*- Encoding: utf-8 -*-
from win007 import cur_match_list, his_match_list, europe


def print_line(title, width=60, token='-'):
    left = (width - len(title)) / 2
    print '%s%s%s' % (
            token*left,
            title,
            token*(width-left-len(title))
            )


def disp_ml(data):
    """[{}, {}, ... ]"""
    for m in data:
        print ',  '.join(['%s: %s' % (k, v) for k, v in m.items()])


# 即将进行的比赛列表
print_line('Current Match List')
ml = cur_match_list()
# disp_ml(ml)
print 'total: %s' % len(ml)


# 历史比赛列表
match_day = '20140712'
print_line('History - Match List')
his_ml = his_match_list(match_day)
# disp_ml(his_ml)
print 'total: %s' % len(his_ml)


def disp_detail(data):
    """{key: [[1, 2, 3, date]]}"""
    for company_id, history in data.items():
        print company_id
        print '\n'.join([', '.join(item) for item in history])

match_id = '1003433'

# 欧赔
print_line('Europe - Match ID: %s' % match_id)
ret = europe(match_id)
disp_detail(ret)
print 'total: %s' % len(ret)
