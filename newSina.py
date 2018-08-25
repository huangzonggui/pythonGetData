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
import json

host = "roll.news.sina.com.cn"

localtime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())#日期
dateStr = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
doc=Document()  #新建文档x
doc.add_paragraph(dateStr)
text = doc.add_paragraph('新浪')

def getNewsHrefs():
    page = 1
    headers = {
        "Referer" : "http://" + host,   #需要添加Referer头部，否则请求失败
        "Accept-Encoding": ""
    }
    
    while  page <= 160:
        req = request.Request(
        "http://" + host + "/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page="+str(page)+"&r=0.6575086962964121",
                              headers = headers
        )
        response = request.urlopen(req)
        jsonData = response.read(50000).decode("gbk")
        ret = re.findall(r",title : \".*?,", jsonData)#?非贪婪匹配
        times = re.findall(r",time : .*?}", jsonData)

        i = 0
        for item in ret: 
            #print (item)
            run = text.add_run('\n'+ item[10:-2] + '  ')
            print (item[10:-2])
            run.font.bold = True#加粗


            timearray = time.localtime(int(times[i][8:-1]))
            otherstyletime = time.strftime("%m-%d %H:%M", timearray)
            run = text.add_run(otherstyletime)
            #print (otherstyletime)
            i=i+1
       
        page = page + 1
    return ret


if __name__ == "__main__":
    getNewsHrefs()

    saveFile=os.getcwd()+"\\新浪"+localtime+".docx"  
    doc.save(saveFile)#根据saveFile的路径和文件名保存文件
