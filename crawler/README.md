数据格式说明
============

# 球探网

#### 即将进行的比赛列表

数据在 bfdata.js 中, 动态加载.

请求 js 文件时, 需要携带时间戳


```javascript
var A=Array(117);
var B=Array(46);
var C=Array(25);
var matchcount=116;
var sclasscount=45;
var matchdate="07月20日";
A[1]="1104348^#D078D8^新加坡联^新加坡聯^SIN D1^幼狮队^幼獅隊^Young Lions^后港联^後港聯^Hougang United FC^19:30^2015,6,20,20,34,00^3^0^2^0^2^0^0^0^1^10^9^0^0^^^^^^/cn/subleague.aspx?sclassid=194^^^^^7-20^2568^4065^^48^0^^2015^1^194^^0".split('^');
A[2]="1090583^#0066FF^中超^中超^CHA CSL^北京国安^北京國安^Beijing Guoan^上海上港^上海上港^Shanghai East Asia FC^19:35^2015,6,20,20,39,28^3^0^0^0^0^0^0^2^0^3^2^1^0^广东体育 北京体育 CCTV5 澳广视体育^1^True^0.25^<a href=http://www.310tv.com/channel/zhongchaozhibo1.html target=_blank><font color=blue>PPTV</font></a>&nbsp;&nbsp;<a href=http://www.310tv.com/channel/cctv5.html target=_blank><font color=blue>CCTV5</font></a>&nbsp;&nbsp;<a href=http://www.310tv.com/channel/guangdongtiyu.html target=_blank><font color=blue>广东体育</font></a>&nbsp;&nbsp;<a href=http://www.310tv.com/channel/beijingtiyu.html target=_blank><font color=blue>北京体育</font></a>^/cn/league.aspx?sclassid=60^^^^^7-20^43^7642^^45^1^;|2;|;|;;;;^2015^1^60^2.5^1".split('^');
```


#### 历史比赛列表

数据在 html 文件中, table 的 body 中.

一条案例数据如下:

```html
<tr height="18" align="center" bgcolor="#F0F0F0" id="tr1_442" name="21,1" infoid="41">
    <td bgcolor="#660033" style="color:white" id="ls_442">美职业</td>
    <td>13日10:00</td>
    <td class="style1">完</td>
    <td align="right">
        <span name="yellow"><img src="/bf_img/yellow2.gif"></span>
        <img src="/bf_img/redcard1.gif">
        <span name="order"><font color="#888888">[7]</font></span>
        温哥华白帽
    </td>
    <td class="style1" style="cursor:pointer;" onclick="showgoallist(942753)">
        <font color="blue">1</font>-<font color="red">3</font>
    </td>
    <td align="left">
        美国芝华士
        <span name="order"><font color="#888888">[14]</font></span>
        <span name="yellow"><img src="/bf_img/yellow1.gif"></span>
    </td>
    <td>
        <font color="red">1</font>-<font color="blue">0</font>
    </td>
    <td style="color:green;">半/一</td>
    <td>2.5</td>
    <td style="word-spacing:-3px" align="left">
        <a href="javascript:" onclick="analysis(942753)">析</a>
        <a href="javascript:" onclick="AsianOdds(942753)" style="margin-left:3px;">亚</a>
        <a href="javascript:" onclick="EuropeOdds(942753)" style="margin-left:3px;">欧</a>
        <a href="javascript:advices(942753)">
            <img src="/image/fx2.gif" alt="网友情报" style="margin-left:3px;">
        </a>
        <img src="/image/zd.gif" alt="走地" style="margin-left:3px;">
    </td>
</tr>
```
