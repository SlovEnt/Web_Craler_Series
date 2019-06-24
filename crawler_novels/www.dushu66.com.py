# -*- coding: utf-8 -*-
__author__ = 'SlovEnt'
__date__ = '2019/6/24 22:07'

import time
import os
from bs4 import BeautifulSoup
from collections import OrderedDict
from chs_tools.get_html_page import get_html_all_content, chrome_get_html_all_content
from chs_tools.print_log import C_PrintLog
from chs_tools.param_info import rtn_parainfo


plog = C_PrintLog()
PARAINFO = rtn_parainfo()
DOWN_FLODERS = PARAINFO["NOVEL_DOWN_FLODERS"]

ROOT_URL = "https://www.dushu66.com" # 网站根目录
GENERAL_PATH = ""       # 通用路径
NOVEL_SUB_ID = "ds13525" # 目录页面ID
ENCODING = "UTF-8" # 页面文字编码
CHAPTER_POST = 1
if GENERAL_PATH == "":
    FULL_URL = "{0}/{1}/".format(ROOT_URL, NOVEL_SUB_ID)
else:
    FULL_URL = "{0}/{1}/{3}/".format(ROOT_URL, GENERAL_PATH, NOVEL_SUB_ID)
plog.debug("小说下载首页为：{0}".format(FULL_URL))


def rtn_chapter_list_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    novelName = soup.find_all(name="div", attrs={"id": "info"})[0].h1.text
    # novelName = novelName.split("《")[1]
    # novelName = novelName.split("》")[0]
    # novelName = "妾本惊华"
    plog.debug("开始下载《{0}》".format(novelName))

    chapterListInfoSoup = soup.find_all(name="dd")
    # print(chapterListInfoSoup)

    chapterListInfoArr = []

    n = 0
    for ddItem in chapterListInfoSoup:
        # print(ddItem)
        n += 1

        if n <= 12:
            continue

        chapterListInfoDict = OrderedDict()
        chapterListInfoDict2 = OrderedDict()

        if "href" not in str(ddItem):
            continue

        if n < CHAPTER_POST:
            continue

        chapterListInfoDict["text"] = ddItem.a.text
        chapterListInfoDict["href"] = ddItem.a["href"]
        chapterListInfoArr.append(chapterListInfoDict)

        # chapterListInfoDict2["text"] = "接"
        # nextPageUrl = ddItem.a["href"].split(".")
        # nextPageUrl = "{0}_2.{1}".format(nextPageUrl[0], nextPageUrl[1])
        # chapterListInfoDict2["href"] = nextPageUrl
        # chapterListInfoArr.append(chapterListInfoDict2)

        plog.tmpinfo(chapterListInfoDict)

    return chapterListInfoArr, novelName

def rtn_chapter_txt(chapterHtml):


    # print("---------------chapterHtml-----------------\n",chapterHtml,"\n\n\n\n")
    # chapterHtml = chapterHtml.replace("<br />", "\n")

    soup = BeautifulSoup(chapterHtml, 'html.parser')

    try:
        soupSub = soup.find_all(name="div", attrs={"class": "content-ext"})[0]
        # soupSubStr = str(soupSub)
        # print("---------------soupSubStr-----------------\n",soupSubStr,"\n\n\n\n")
        # soupSubStr = "{0}{1}".format(soupSubStr.split("<div")[0],"</article>")

        # soupSub = BeautifulSoup(soupSubStr, 'html.parser')

        txtContent = soupSub.text
        txtContent = txtContent.replace("    ", "")
        txtContent = txtContent.replace("                ", "")
        txtContent = txtContent.replace("\n\n", "\n")
        txtContent = txtContent.replace("\n                    -->>本章未完，点击下一页继续阅读", "")
        txtContent = txtContent.replace("\n    -->>本章未完，点击下一页继续阅读", "")

        print(txtContent)
        return txtContent

    except:
        time.sleep(2)
        print("--------------- chapterHtml error -----------------\n", chapterHtml)
        return False

def write_txt_content(txtFileName, chapterName, chapterTxt, encoding):
    with open(txtFileName, 'a', encoding=encoding) as f:
        if chapterName == "接":
            pass
        else:
            f.write(chapterName + "\n")
        # print(chapterTxt)
        f.write(chapterTxt)

if __name__ == '__main__':

    html = get_html_all_content(FULL_URL, "info", ENCODING)

    # 返回章节信息
    chapterListInfo, novelName = rtn_chapter_list_info(html)

    novelFilePath = r"{0}\{1}.txt".format(DOWN_FLODERS, novelName)

    if CHAPTER_POST == 1:
        if (os.path.exists(novelFilePath)):
            os.remove(novelFilePath)

    for chapterInfo in chapterListInfo:

        chapterUrl = "{0}{1}".format(ROOT_URL, chapterInfo["href"])

        plog.debug("网址：{0}，页面章节标题：{2}，文件路径：{1} ！！！".format(chapterUrl, novelFilePath, chapterInfo["text"]))

        chapterHtml = get_html_all_content(chapterUrl, "content-ext", ENCODING)

        chapterTxt = rtn_chapter_txt(chapterHtml)
        # print(str(chapterHtml))

        if chapterTxt is not False:
            write_txt_content(novelFilePath, chapterInfo["text"], chapterTxt, ENCODING)
        else:
            plog.error("获取失败！！！！！！")
