
from urllib import request
import requests
import time
import sys
import re
from bs4 import BeautifulSoup

linkHost = "https://www.168wujin.wang"
link = "https://www.168wujin.wang/jintelang/album/705/detail?staff_id=1583&hide=&show_contact=&show_dir=1"
homeLink = "https://www.168wujin.wang/jintelang/album?staff_id=1583&hide=&show_contact=&show_dir=1#706" # 首頁


linkList = []

def getLink(): 
    global linkList
    #  print(soup.find(class='wrapper'))
    #  ulString = soup.find(
    #      "ul",
    #      {"class": "toggle-wrap catalog-list"}
    #  )
    # ulString = soup.find_all('a', href=True)
    # print(ulString)
    hostBase = "www.168wujin.wang"
    headersBase = {#为什么将这个头放在while外面不行？？？第二个以后的请求都是Access defined
        "Referer" : "http://" + hostBase,   #需要添加Referer头部，否则请求失败
        "Accept-Encoding": ""
    }
    req = request.Request(
        homeLink,
                          headers = headersBase
    )
    response = request.urlopen(req)
    jsonData = response.read().decode("utf-8")
    jsonData = jsonData.replace('\\', '')
    # ret = re.findall(r"a href=\"javascript:void (0)\" data-size=\"1458x2000\".+?style=\"pointer-events: none\"", jsonData)
    #    ret = re.findall(r".htm\\\">.*?<\\/a>", str(jsonData))#?非贪婪匹配
        # times = re.findall(r"t-time\\\">.*?<\\/span>", str(jsonData))
    # ret = re.findall(r"data.*?.jpg", jsonData)
    # print(jsonData)
    ret = re.findall(r"/jintelang/album.*?.show_dir=1", jsonData)
    titleList = re.findall(r"<span>.*?</span>", jsonData)

    # for titleItem in titleList:
    #     print(titleItem)

    i=0
    for item in ret:
        if len(titleList) > i:
            # print (titleList[i])
            # getData(item, title)
            # getData(item) # 第一種方式
            getByMultiTag(item) # 第二種方式
            i+=1


def getData(getByLink):
   
    host = "www.168wujin.wang"
    headers = {#为什么将这个头放在while外面不行？？？第二个以后的请求都是Access defined
        "Referer" : "http://" + host,   #需要添加Referer头部，否则请求失败
        "Accept-Encoding": ""
    }
    req = request.Request(
        linkHost + getByLink,
                          headers = headers
    )
    response = request.urlopen(req)
    jsonData = response.read().decode("utf-8")
    jsonData = jsonData.replace('\\', '')
    # ret = re.findall(r"a href=\"javascript:void (0)\" data-size=\"1458x2000\".+?style=\"pointer-events: none\"", jsonData)
    #    ret = re.findall(r".htm\\\">.*?<\\/a>", str(jsonData))#?非贪婪匹配
        # times = re.findall(r"t-time\\\">.*?<\\/span>", str(jsonData))
    # ret = re.findall(r"data.*?.jpg", jsonData)
    # print(jsonData)
    ret = re.findall(r"<a href=.*?.jpg", jsonData)

    # i = 0
    # print(ret)
    for item in ret:
        temp = item.split('"')
        tempString = "<li> <img src=\\\"" + temp[5] + "\\\" style=\\\"pointer-events: none;width: 100%\\\"></li>"
        # print (temp[5])
        print (tempString)
        # print (re.find(r"https:.*?.jpg", item))
        # i = i + 1

def getByMultiTag(itemLink): 
    response = requests.get(linkHost + itemLink)
    soup = BeautifulSoup(response.text, "html.parser")

    imgList = soup.find_all(attrs={"data-med-size": "1458x2000"})
    # imgList = soup.find_all(attrs={"href": "javascript:void (0)"})


    # ulString = soup.find_all('a', href=True) 
    for item in imgList: print (item)


getLink()
# getByMultiTag()