# -*- coding: utf-8 -*-

'''
功能:抓取腾讯财经新闻内容并保存为pdf格式文件，目前只抓取首页50条新闻
用法:python3 tencentNews.py filename.pdf
Python版本:Python3
依赖第三方库：bs4,pdfkit
依赖第三方软件:wkhtmltopdf
'''

#author:王得伟Dewitt
#email:wangdewei1996@163.com
#date:2017.09.05

from urllib import request
import os  
import re
import sys
from bs4 import BeautifulSoup
import pdfkit
from docx import Document  
from docx.shared import Inches 
from docx.shared import Pt
import time  # 引入time模块

host = "roll.finance.qq.com"

localtime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())#日期
dateStr = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
# 格式化成2016-03-20 11:45:39形式
#localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
doc=Document()  #新建文档
##word title  
doc.add_paragraph(dateStr)
text = doc.add_paragraph('腾讯财经')
#doc.add_heading('腾讯财经',0)

def wirteToDoc():
    '''
    向后台发起请求，把需要的内容写入docx文档中
    '''
    i=1
    while i <= 14:
        print(i)
        time.sleep(0.5)
        headers = {#为什么将这个头放在while外面不行？？？第二个以后的请求都是Access defined
            "Referer" : "http://" + host,   #需要添加Referer头部，否则请求失败
            "Accept-Encoding": ""
        }
        req = request.Request(
            "http://" + host + "/interface/roll.php?0.7895971873270728&cata=&site=finance&date=&page="+str(i)+"&mode=1&of=json",
                              headers = headers
        )
        response = request.urlopen(req)
        jsonData = response.read().decode("gbk")
        jsonData = jsonData.replace('\\', '')
        #print(jsonData)
        ret = re.findall(r"http://.+?\.htm", jsonData)
                        #http://finance.qq.com/a/20180223/025599.htm
        #print(ret)#ret是新闻链接URL list
        headers = {
            "Accept-Encoding": ""
        }
        for href in ret:
            req = request.Request(
                href,
                headers=headers
            )
            response = request.urlopen(req)#请求数据后的响应
            #print(str(response))
            #TODO:存在某些页面无法解码，原因不明，暂时忽略
            html = response.read().decode("gb2312", "ignore")
            bsObj = BeautifulSoup(html, "html.parser")
            page = bsObj.find(
                "div",
                {"class": "qq_article"}
            )#一页全部内容
            if page:#在一页里面拿我想要的
                title = page.find("h1")
                timeStr = page.find(
                    "span",
                    {"class": "a_time"}
                )
                titdd = page.find(#摘要
                    "p",
                    {"class": "titdd-Article"}
                )

                run = text.add_run('\n'+str(title.string))
                #paragraph_format.line_spacing = Pt(18)
                #run = paragraph.add_run(str(timeStr.string)[6:16])#段落后add_run不换行
                run.font.size = Pt(11)
                run.font.bold= True#加粗

                run = text.add_run(str(timeStr.string)[6:16])#时间
                run.font.size = Pt(9)
                run.italic = True#斜体

                if titdd!=None:
                    run = text.add_run('\n'+str(titdd.get_text()))#摘要
                    run.font.size = Pt(9)
                    #doc.add_paragraph('')
                    #doc.add_paragraph(str(title) + str(timeStr) + str(titdd))
        i = i + 1

if __name__ == "__main__":
    wirteToDoc()#把标题时间抽取出来放在doc中
    #word  
    saveFile=os.getcwd()+"\\腾讯财经"+localtime+".docx"  
    doc.save(saveFile)#根据saveFile的路径和文件名保存文件
