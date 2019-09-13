# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/18 12:39'

import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from chs_tools.get_html_page import get_html_all_content, chrome_get_html_all_content

'''
https://www.sto.cx
'''

# 单一小说网址
novelId = "book-108725-1.html"
ROOT_URL = "https://www.sto.cx/{0}".format(novelId)
DOWN_FLODERS = r"E:\下载小说"

def rtn_chapter_list_info(html):

    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"class": "bookbox"})[0].h1.text
    # novelName = novelName.replace("\n", "")
    novelName = novelName.strip()
    novelName = novelName.split("《")[1]
    novelName = novelName.split("》")[0]
    print(novelName)

    chapterListInfoSoup = soup.find_all(name="select", attrs={"id": "Page_select"})[0].find_all(name="option")

    chapterListInfoArr = []

    for ddItem in chapterListInfoSoup:

        chapterListInfoDict = OrderedDict()
        # print(str(ddItem))
        patt = re.compile(r'<option value="/(.+?)">(.+?)</option>')
        option = patt.findall(str(ddItem))
        # print(option)

        chapterListInfoDict["text"] = option[0][1]
        chapterListInfoDict["href"] = option[0][0]
        # print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName


def rtn_chapter_txt(chapterHtml):
    html = str(chapterHtml)

    patt = re.compile(r'''(<span id="a_d_\d">.+?</span>)''', re.S)
    spans =  patt.findall(html)

    for span in spans:
        html = html.replace(span, "")

    soup = BeautifulSoup(html, 'html.parser')

    txtContent = soup.find_all(name="div", attrs={"id": "BookContent"})[0]

    txtContent = str(txtContent).replace("<br/>", "\n")

    # print(txtContent)
    # time.sleep(2000)
    txtContent = BeautifulSoup(txtContent, 'html.parser').text
    # txtContent = txtContent.text
    txtContent = txtContent.replace(' ', '')
    txtContent = txtContent.replace('　　', '')
    txtContent = txtContent.replace('本书由本站首发，请勿转载！◎思◎兔◎在◎线◎阅◎读◎', '')
    txtContent = txtContent.replace('本书由本站首发，请勿转载！', '')
    txtContent = txtContent.replace('本书由首发，请勿转载！', '')
    txtContent = txtContent.replace('()', '')
    txtContent = txtContent.replace('*作*品*由*思*兔*在*線*閱*讀*網*友*整*理*上*傳*', '')
    txtContent = txtContent.replace('严禁附件中包含其他网站的广告本文已阅读完毕，欢迎发表书评！', '')
    txtContent = txtContent.replace('(adsbygoogle = window.adsbygoogle || []).push({});', '')
    txtContent = txtContent.replace('(adsbygoogle=window.adsbygoogle||[]).push({});', '')
    txtContent = txtContent.replace('\n\n', '\n')
    txtContent = txtContent.replace('\n\n', '\n')
    txtContent = txtContent.replace('\n\n', '\n')
    txtContent = txtContent.replace('\n\n', '\n')
    txtContent = txtContent.replace('\n\n\n', '\n')
    txtContent = txtContent.replace('☆、', '\n')
    # txtContent = txtContent.replace('\ue4c6','')
    # txtContent = txtContent.replace('\ue0d8','')
    # print(txtContent)

    return txtContent


def write_txt_content(txtFileName, chapterName, chapterTxt):
    with open(txtFileName, 'a', encoding="utf-8") as f:
        # f.write(chapterName + "\n")
        f.write(chapterTxt + "\n\n")

if __name__ == '__main__':

    html = chrome_get_html_all_content(ROOT_URL, "bookbox")

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)
    novelName = novelName.replace("/", "-")

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if os.path.exists(novelFilePath):
        os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:
        # print(chapterInfo)

        chapterUrl = "{0}/{1}".format("https://www.sto.cx", chapterInfo["href"])
        print(chapterUrl)

        chapterHtml = chrome_get_html_all_content(chapterUrl, "BookContent")
        # print(chapterHtml)
        chapterTxt = rtn_chapter_txt(chapterHtml)
        print(chapterTxt)

        print("路径：{0}，正在获取 章节：{1} ！！！".format(novelFilePath, chapterInfo["text"]))

        write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt)
