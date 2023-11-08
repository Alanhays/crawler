# --*-- coding: utf-8 --*--
# @Author  : 微信公众号：网络爬虫逆向交流

import json
import re
import requests
import execjs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}

url = ""

sess = requests.session()
# 第一次请求 获取 __jsluid_s

res = sess.get(url=url, headers=headers)
content = re.findall('cookie=(.*?);location', res.text)[0]
__jsl_clearance_s = execjs.eval(content).split(';')[0]
sess.cookies.update({"__jsl_clearance_s": __jsl_clearance_s.split("=")[1]})

# 第二次请求 获取参数
res = sess.get(url=url, headers=headers)
go_params = re.findall(';go\((.*?)\)</script>', res.text)[0]
params = json.loads(go_params)

# 加载加密函数
with open('jsl.js', 'r', encoding='utf-8') as f:
    jsl_js = f.read()
# 传入参数
cookie = execjs.compile(jsl_js).call('JSL', params)
sess.cookies.update(cookie)

# 第三次请求
res = sess.get(url=url, headers=headers)
res.encoding = 'utf-8'
print(res.text)
