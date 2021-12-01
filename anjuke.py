# -*- coding:utf-8 -*-
import requests
import random
from requests.exceptions import RequestException
from time import sleep
import csv
from urllib import request as urlrequest
import ssl
from lxml import etree
import re
import threading
from bs4 import BeautifulSoup
from urllib.request import ProxyHandler,build_opener
import requests


# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

districts = ['jingan', 'xuhui', 'huangpu', 'changning', 'putuo', 'pudong', 'baoshan', 'qingpu',
             'hongkou', 'yangpu', 'minhang', 'jinshan', 'jiading', 'chongming', 'fengxian', 'songjiang', 'shanghaizhoubian']
uncatched = ['songjiang', 'shanghaizhoubian']


def write_to_file(content):
    with open('anjuke-result-11-19.csv', 'a',encoding='utf-8', newline='') as csvfile:
        headings = ["price", "district", "bizCircle",
                    "area", "address", "roomNumber", "floor",  "url", "title", "human",
                     "type1", "type2", "type3", "type4"]
        writer = csv.DictWriter(
            csvfile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        for row in content:
            writer.writerow(row)
        csvfile.close()


# 获取页面
def get_page(url):
    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'
}
    page = requests.get(url, headers=headers)
    html = page.text
    return html



def parse_page(html):
    soup = BeautifulSoup(html, features="lxml")
    result = []
    for content in soup.find_all("div", "zu-itemmod"):
        try:
            head = content.find("h3")
            url = head.find("a")["href"]
            title = head.find("b").contents[0]
            human = content.find("p", "details-item tag").contents[11].strip()
            op = ""
            for item in content.find("p", "details-item tag").contents:
                try:
                    if item.contents[0] == '\ue147':
                        break
                    op += item.contents[0]
                except:
                    op += item
            op = op.strip()   # '1室1厅|38.1平米|中层(共6层)'
            location = content.find("address").find("a").contents[0] # 紫云小区
            address =  content.find("address").contents[-1].strip() # 上海周边-湖州 紫云一路,近大东路

            tags = content.find("p", "details-item bot-tag").contents # 分别是出租类型，方位，有无电梯，地铁线 ['\n',<span class="cls-1">整租</span>, '\n', <span class="cls-2">朝南</span>, '\n']
            type1, type2, type3, type4 = "", "", "", "" 
            try:
                type1 = tags[1].contents[0]
                type2 = tags[3].contents[0]
                type3 = tags[5].contents[0]
                type4 = tags[7].contents[0]
            except:
                pass
            price = content.find("div", "zu-side").find("b").contents[0]

            result.append({
                "price": price, # 价格
                "district": soup.find("div","zu-sort").find("em").contents[0], # 静安区
                "bizCircle": location, #商圈
                "area": op.split("|")[1], # 面积
                "address": address, 
                "roomNumber": op.split("|")[0], #房间数
                "floor": op.split("|")[2], #楼层
                "url": url, 
                "title": title,
                "human": human,
                "type1": type1,
                "type2": type2,
                "type3": type3,
                "type4": type4,
            })
        except:
            print("something wrong")
            pass
    # print(result)
    return result


def main():
    for district in uncatched:
        url = 'https://sh.zu.anjuke.com/fangyuan/'+district+'/'
        for page in range(1, 3000):
            print('正在爬取第'+ str(page) + '页    ', end='')
            print(url + "p" + str(page) + "/")
            html = get_page(url + "p" + str(page) + "/")
            if "您要查看的页面丢失了" in html or "访问过于频繁" in html:
                break
            result = parse_page(html)
            write_to_file(result)
            sleep(10)



if __name__ == '__main__':
    main()
