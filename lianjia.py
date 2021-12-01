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

districts = ['jingan', 'xuhui', 'huangpu', 'changning', 'putuo', 'pudong', 'baoshan', 'zhabei',
             'hongkou', 'yangpu', 'minhang', 'jinshan', 'jiading', 'chongming', 'fengxian', 'songjiang']

# districts = ['xihu', "xiacheng", "jianggan",
#              "gongshu", "shangcheng", "binjiang"]





def write_to_file(content):
    with open('result-11-19.csv', 'a',encoding='utf-8') as csvfile:
        headings = ["price", "district", "bizCircle",
                    "area", "direction", "roomType", "roomNumber", "floor",  "url"]
        writer = csv.DictWriter(
            csvfile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        for row in content:
            writer.writerow(row)
        csvfile.close()


# 获取页面
def get_page(url):
    # proxy = random.choice(availabe_proxies)
    # proxy_hander = ProxyHandler(proxy)
    # opener = build_opener(proxy_hander)
    # print(url)
    # page = opener.open(url)
    headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'
}
    page = requests.get(url, headers=headers)
    html = page.text
    return html


def parse_page_size(html):
    soup = BeautifulSoup(html, features="lxml")
    total = soup.find("span", "content__title--hl")
    return int(total.contents[0])


def parse_page(html):
    soup = BeautifulSoup(html, features="lxml")
    result = []
    for content in soup.find_all("div", "content__list--item"):
        try:
            url = content.find(
                "p", "content__list--item--title").find("a")['href']
            des = content.find("p", "content__list--item--des")
            desContents = des.contents
            price = content.find(
                "span",
                "content__list--item-price"
            ).find("em").contents[0]
            district = des.find_all("a")[0].contents[0]
            bizCircle = des.find_all("a")[1].contents[0]
            area = desContents[5].contents[0]
            direction = desContents[8].strip("\n").strip(" ")
            roomType = desContents[10].strip("\n").strip(" ")
            roomNumber = desContents[12].strip("\n").strip(" ")
            floor = desContents[13].contents[-1].strip("\n").strip(" ").replace(" ","")
            result.append({
                "price": price,
                "district": district,
                "bizCircle": bizCircle,
                "area": area,
                "direction": direction,
                "roomType": roomType,
                "roomNumber": roomNumber,
                "floor": floor,
                "url": url,
            })
        except:
            print("something wrong")
            pass
    # print(result)
    return result


def main():
    for district in districts:
        url = 'https://sh.lianjia.com/zufang/'+district+'/'
        html = get_page(url)
        size = int(parse_page_size(html) / 30)
        print(size)
        for page in range(1, size):
            print('正在爬取第'+ str(page) + '页')
            url = 'http://sh.lianjia.com/zufang/' + \
                district + '/pg' + str(page)
            html = get_page(url)
            result = parse_page(html)
            write_to_file(result)
            sleep(2)



if __name__ == '__main__':
    main()
