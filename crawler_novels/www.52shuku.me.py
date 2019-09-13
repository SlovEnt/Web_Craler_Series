# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/5/11 9:26'

'''
https://www.52shuku.me/
'''

import time
import os
import re
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
# import sys
# sys.path.append('.')
from chs_tools.get_html_page import get_html_all_content, chrome_get_html_all_content


NOVEL_SUB_ID = "yanqing/0719" # 目录子页面
NOVEL_PAGE = "hwY2.html" # 目录子页面

ROOT_URL = "https://www.52shuku.me" # 网站根目录

FULL_URL = "{0}/{1}/{2}".format(ROOT_URL, NOVEL_SUB_ID, NOVEL_PAGE)
CHAPTER_POST = 1

DOWN_FLODERS = r"E:\下载小说"



def rtn_chapter_list_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="h1", attrs={"class": "article-title"})[0].text
    print("开始下载《{0}》".format(novelName))

    chapterListInfoSoup = soup.find_all(name="ul", attrs={"class": "list"})[0].find_all(name="li")

    chapterListInfoArr = []

    n = 0
    for ddItem in chapterListInfoSoup:
        n += 1
        chapterListInfoDict = OrderedDict()

        if "href" not in str(ddItem):
            continue

        if n < CHAPTER_POST:
            continue

        chapterListInfoDict["text"] = ddItem.a.text
        chapterListInfoDict["href"] = ddItem.a["href"]
        # print(chapterListInfoDict)

        chapterListInfoArr.append(chapterListInfoDict)

    return chapterListInfoArr, novelName


def rtn_chapter_txt(chapterHtml):


    # print("---------------chapterHtml-----------------\n",chapterHtml,"\n\n\n\n")
    chapterHtml = chapterHtml.replace("           </p>","")

    soup = BeautifulSoup(chapterHtml, 'html.parser')

    try:
        soupSub = soup.find_all(name="article", attrs={"class": "article-content"})[0]
        soupSubStr = str(soupSub)
        # print("---------------soupSubStr-----------------\n",soupSubStr,"\n\n\n\n")
        soupSubStr = "{0}{1}".format(soupSubStr.split("<div")[0],"</article>")

        soupSub = BeautifulSoup(soupSubStr, 'html.parser')

        txtContent = soupSub.text
        txtContent = txtContent.replace("　　", "")
        txtContent = txtContent.replace("\n\r", "")
        txtContent = txtContent.replace("【52书库将分享完结好看的言情小说以及耽美小说等，找好看的小说就来52书库http://www.52shuku.me/】  ", "")

        print(txtContent)
        return txtContent

    except:
        time.sleep(2)
        print("--------------- chapterHtml error -----------------\n", chapterHtml)
        return False

def write_txt_content(txtFileName, chapterName, chapterTxt, encoding):
    with open(txtFileName, 'a', encoding=encoding) as f:
        # f.write(chapterName + "\n")
        f.write(chapterTxt)


if __name__ == '__main__':

    html = chrome_get_html_all_content(FULL_URL, "article-title", "UTF-8")

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if CHAPTER_POST == 1:
        if (os.path.exists(novelFilePath)):
            os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:

        # print(chapterInfo)

        chapterUrl = "{2}".format(ROOT_URL, NOVEL_SUB_ID, chapterInfo["href"])

        print("网址：{0}，页面章节标题：{2}，文件路径：{1} ！！！".format(chapterUrl, novelFilePath, chapterInfo["text"]))

        chapterHtml = chrome_get_html_all_content(chapterUrl, "article-content", "UTF-8")

        chapterTxt = rtn_chapter_txt(chapterHtml)

        if chapterTxt is not False:
            write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt, "UTF-8")
        else:
            print("获取失败！！！！！！")
