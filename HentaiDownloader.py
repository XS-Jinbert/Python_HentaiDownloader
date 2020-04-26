# -*- coding = utf-8 -*-
# by XS-Jinbert
# only can download from https://asmhentai.com/

from bs4 import BeautifulSoup
import requests
import os
import re

def main():
    # url = "https://images.asmhentai.com/010/297225/3.jpg"
    Imageurl = "https://images.asmhentai.com"
    Bookurl = "https://asmhentai.com/g/"
    findHentaiBook(Bookurl)


findPage = re.compile(r'<h3>Pages: (.*?)</h3>')
findArtists = re.compile(r'<div class="tag_list"><a href="/artists/name/(.*)/"><span class="badge tag">')
findTitle = re.compile(r'<h2>(.*?)</h2>')
findNumber = re.compile(r'images.asmhentai.com/(.*?)/')

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
        # print(right)

        title = re.findall(findTitle, right)
        page = re.findall(findPage, right)
        artists = re.findall(findArtists, right)
        title[0] = title[0].replace("/", "")
        print(title[0])
        print(page[0])
        print(artists[0])

        print("解析完成")
        findpage(numberURL=Imageurl, sumpage=page[0], root=title[0])


    except Exception as e:
        print("解析失败:" + str(e))


def findpage(numberURL, sumpage, root):
    print("本子：" + root + " 共" + sumpage + "张图片，开始下载ing")
    sumpage = int(sumpage)
    for i in range(1, sumpage+1):
        pageURL = numberURL+str(i)+".jpg"
        print(pageURL)
        download(pageURL, root)
        print("第" + str(i) + "已下载！")
    print("该本子下载完成")

def findDownloadNumber(html):
    soup = BeautifulSoup(html, "html.parser")
    ImageLink = soup.find_all('img', class_="lazy no_image")
    ImageLink = str(ImageLink)
    DownloadNumber = re.findall(findNumber, ImageLink)
    return DownloadNumber[0]

def download(url, fileroot):
    root = "D://HentaiDownloader/"+fileroot+"//"
    path = root + url.split("/")[-1]
    try:
        if not os.path.exists(root):    # 如果文件夹不存在则创建文件
            os.mkdir(root)
        if not os.path.exists(path):    # 如果文件夹存在开始爬取
            r = requests.get(url)       # 发起请求
            r.raise_for_status()        # 返回状态
            # 使用with语句可以不用自己手动关闭已经打开的文件流
            with open(path, "wb") as f: # 开始写文件，wb代表写二进制文件
                f.write(r.content)
        else:  # 重复爬则提醒
            print("文件已存在")
    except Exception as e:
        print("爬取失败:" + str(e))

if (__name__ == "__main__"):
    main()
