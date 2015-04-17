足球比赛分析
============

#### 使用说明

###### 交互式

```shell
$ python football.py
url: 
```

根据提示输入网址即可

###### 带参数的命令

```shell
$ python football.py http://zq.win007.com/analysis/1090590sb.htm
```

###### 忽略比赛类型

如果需要忽略个别类型的比赛,  
在 football.py 同级目录下创建文件: `match_ignore.ini`  
在文件中添加需要忽略的比赛类型.  
一行一个比赛类型.

例如:

```shell
球会友谊
友谊赛
球會友誼
```


#### 开发环境

```shell
$ pip install -r requirements.txt
```
