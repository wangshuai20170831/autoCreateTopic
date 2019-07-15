#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:wpaifang
# datetime:2019/7/15 9:36
# software: PyCharm
# function:
import urllib

import requests
import re
import json
from bs4 import BeautifulSoup as bs

book = ['/wordbook/106306/', '/wordbook/106300/', '/wordbook/106312/',
        '/wordbook/106330/', '/wordbook/106360/']

original_link = 'https://www.shanbay.com'  # 扇贝单词/单词书 链接
book_link = original_link + '/wordbook/106360/'

sess = requests.session()
sess.headers[
    'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/34.0.1847.131 Safari/537.36 '

# sess.proxies = {"https": "47.100.104.247:8080", "http": "36.248.10.47:8080", }#
sess.keep_alive = False
try:
    res = sess.get(book_link)
except Exception as err:
    print(err)
###
# 1. 访问一本书 爬去所有单元的单词和词组链接
# 2. 依次访问链接 每次访问时 先判断有几页
# 3. 然后对每一页进行爬取
###
content = bs(res.text, 'html.parser')
# print(content)
wordLink = []
wordLink_name = []
pageLink = []
word_list = []
trans_list = []
if content.select('.wordbook-wordlist-name'):
    for item in content.select('.wordbook-wordlist-name'):
        wordLink_name.append(item.text.replace('\n', ''))
        for a in item.select("a"):
            wordLink.append(a['href'])

for i in range(0, len(wordLink)):  # 每单元的单词链接
    word_link = wordLink[i]
    word_belong = wordLink_name[i]  # 用作文件名
    try:
        res = sess.get(original_link + word_link)
    except Exception as err:
        print(err)
    content = bs(res.text, 'html.parser')
    if content.select('.table-striped'):  # 获取遍历单元的第一页单词和翻译
        for content1 in content.select('.table-striped'):
            for content2 in content1.select('.span2'):  # 单词
                word_list.append(content2.text)
            for content3 in content1.select('.span10'):  # 翻译
                trans = content3.text.split('.')
                if len(trans) == 2:
                    trans_list.append(trans[1])
                elif len(trans) == 3:
                    trans_list.append(trans[2])
                else:
                    trans_list.append(trans[0])
    for item in range(2, 11):
        try:
            res = sess.get(original_link + word_link + '?page=' + str(item))
        except Exception as err:
            break
        content = bs(res.text, 'html.parser')
        if content.select('.table-striped'):  # 获取遍历单元的后几页的单词和翻译
            for content1 in content.select('.table-striped'):
                for content2 in content1.select('.span2'):  # 单词
                    word_list.append(content2.text)
                for content3 in content1.select('.span10'):  # 翻译
                    trans = content3.text.split('.')
                    if len(trans) == 2:
                        trans_list.append(trans[1])
                    elif len(trans) == 3:
                        trans_list.append(trans[2])
                    else:
                        trans_list.append(trans[0])
    with open(word_belong + '.txt', 'w', encoding='utf-8') as f:
        for item in word_list:
            f.write(item + '\n')
        for item in trans_list:
            f.write(item + '\n')
    word_list = []
    trans_list = []
# print(word_list)
# print(trans_list)
