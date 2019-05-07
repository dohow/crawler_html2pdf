# coding=utf-8
from __future__ import unicode_literals

import logging
import os
import re
import time
import json

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""

options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
htmls = []
urls = [u'http://www.liaoxuefeng.com/wiki/896043488029600', u'http://www.liaoxuefeng.com/wiki/896043488029600/896067008724000', u'http://www.liaoxuefeng.com/wiki/896043488029600/896202815778784', u'http://www.liaoxuefeng.com/wiki/896043488029600/896202780297248', u'http://www.liaoxuefeng.com/wiki/896043488029600/896067074338496', u'http://www.liaoxuefeng.com/wiki/896043488029600/896827951938304', u'http://www.liaoxuefeng.com/wiki/896043488029600/896954074659008', u'http://www.liaoxuefeng.com/wiki/896043488029600/897013573512192', u'http://www.liaoxuefeng.com/wiki/896043488029600/897271968352576', u'http://www.liaoxuefeng.com/wiki/896043488029600/897884457270432', u'http://www.liaoxuefeng.com/wiki/896043488029600/897889638509536', u'http://www.liaoxuefeng.com/wiki/896043488029600/900002180232448', u'http://www.liaoxuefeng.com/wiki/896043488029600/896954117292416', u'http://www.liaoxuefeng.com/wiki/896043488029600/898732864121440', u'http://www.liaoxuefeng.com/wiki/896043488029600/898732792973664', u'http://www.liaoxuefeng.com/wiki/896043488029600/896954848507552', u'http://www.liaoxuefeng.com/wiki/896043488029600/900003767775424', u'http://www.liaoxuefeng.com/wiki/896043488029600/900004111093344', u'http://www.liaoxuefeng.com/wiki/896043488029600/900005860592480', u'http://www.liaoxuefeng.com/wiki/896043488029600/900388704535136', u'http://www.liaoxuefeng.com/wiki/896043488029600/900394246995648', u'http://www.liaoxuefeng.com/wiki/896043488029600/900375748016320', u'http://www.liaoxuefeng.com/wiki/896043488029600/1216289527823648', u'http://www.liaoxuefeng.com/wiki/896043488029600/900788941487552', u'http://www.liaoxuefeng.com/wiki/896043488029600/902335212905824', u'http://www.liaoxuefeng.com/wiki/896043488029600/902335479936480', u'http://www.liaoxuefeng.com/wiki/896043488029600/900937935629664', u'http://www.liaoxuefeng.com/wiki/896043488029600/1163625339727712', u'http://www.liaoxuefeng.com/wiki/896043488029600/900785521032192', u'http://www.liaoxuefeng.com/wiki/896043488029600/900004590234208', u'http://www.liaoxuefeng.com/wiki/896043488029600/898732837407424', u'http://www.liaoxuefeng.com/wiki/896043488029600/899998870925664', u'http://www.liaoxuefeng.com/wiki/896043488029600/900062620154944']

for index, url in enumerate(urls):
    html = parse_body(self.request(url))
    f_name = ".".join([str(index), "html"])
    with open(f_name, 'wb') as f:
        f.write(html)
    htmls.append(f_name)
print(htmls)
pdfkit.from_url(htmls, self.name + ".pdf", options=options)

def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_="x-wiki-content")[0]

            # 加入标题, 居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(2).startswith("http"):
                    rtn = "".join([m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = html_template.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)