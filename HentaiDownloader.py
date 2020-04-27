# -*- coding = utf-8 -*-
# by XS-Jinbert
# only can download from https://asmhentai.com/

from bs4 import BeautifulSoup
import requests
import time
import os
import re

findPage = re.compile(r'<h3>Pages: (.*?)</h3>')
findArtists = re.compile(r'<div class="tag_list"><a href="/artists/name/(.*)/"><span class="badge tag">')
findTitle = re.compile(r'<h2>(.*?)</h2>')
findNumber = re.compile(r'images.asmhentai.com/(.*?)/')

def main():
    Imageurl = "https://images.asmhentai.com"
    Bookurl = "https://asmhentai.com/g/"
    findHentaiBook(Bookurl)

# 寻找本子链接并解析
def findHentaiBook(Bookurl):
    BookNumber = input("请输入要下载的本子编号：")
    BookURL = Bookurl + BookNumber
    html = ""
    try:
        print("解析ing")
        r = requests.get(BookURL)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        Imageurl = "https://images.asmhentai.com/" + findDownloadNumber(html) + "/" + BookNumber + "/"
        right = soup.find_all('div', class_="right")
        right = str(right)

        title = re.findall(findTitle, right)        # 正则表达式收集日文/中文标题
        page = re.findall(findPage, right)          # 正则表达式收集本子页码
        artists = re.findall(findArtists, right)    # 正则表达式收集本子作者
        title[0] = title[0].replace("/", "")
        print("标题为"+title[0])
        print("共"+page[0]+"页")
        if(len(artists) > 0):
            print("作者："+artists[0])
            title[0] = title[0] + " Artists[" + artists[0] + "]"    # 拼接作者至文件尾部
        else:
            print("作者不明")
        print("解析完成")
        findpage(numberURL=Imageurl, sumpage=page[0], root=title[0])

    except Exception as e:
        print("解析失败:" + str(e))

# 每本本子图片下载
def findpage(numberURL, sumpage, root):
    print("本子：" + root + " 共" + sumpage + "张图片，开始下载ing")
    sumpage = int(sumpage)

    start = time.time()     # 记录下载开始时间
    F = {}                  # 记录下载失败页

    for i in range(1, sumpage+1):
        pageURL = numberURL+str(i)+".jpg"       # 获取图片页链接
        # print(pageURL)
        print("第" + str(i) + "下载ing...")
        a = download(pageURL, root, i)          # 下载图片
        if(a == False):
            F[i] = pageURL
    end = time.time()       # 记录下载结束时间
    print("该本子下载完成，共用时："+str(end-start)+"s")
    if(len(F) > 0):
        print("其中下载错误页有："+str(F))
    else:
        print("下载过程无图片页下载错误")

# 寻找本子所在服务器
def findDownloadNumber(html):
    soup = BeautifulSoup(html, "html.parser")
    ImageLink = soup.find_all('img', class_="lazy no_image")
    DownloadNumber = re.findall(findNumber, str(ImageLink))
    return DownloadNumber[0]

# 下载每张图片
def download(url, fileroot, n):
    root = "D://HentaiDownloader/"+fileroot+"//"
    path = root + str(n).zfill(4)+".jpg"                    # 路径+文件名（字符串对象.zfill()对字符串自动补0）
    try:
        if not os.path.exists("D://HentaiDownloader//"):
            os.mkdir("D://HentaiDownloader//")
        if not os.path.exists(root):                        # 如果文件夹不存在则创建文件
            os.mkdir(root)
        if not os.path.exists(path):                        # 如果文件夹存在开始爬取
            r = requests.get(url, timeout=20)               # 发起请求
            r.raise_for_status()                            # 返回状态
            # 使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path, "wb") as f:                     # 开始写文件，wb代表写二进制文件
                f.write(r.content)
                print("第" + str(n) + "下载成功！")
        else:  # 重复爬则提醒
            print("文件已存在")
        return True
    except Exception as e:
        print("爬取失败:" + str(e))
        return False

if (__name__ == "__main__"):
    main()
