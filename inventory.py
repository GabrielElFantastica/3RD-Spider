# -*- coding = utf-8 -*-
# @Time : 2022-04-08 10:21
# @Author : 帅哥张
# @File : inventory.py
# @Software: PyCharm
import re
from typing import Any
import datetime
import requests
from bs4 import BeautifulSoup

find_inventory = re.compile(r'<option value="(\d*)">', re.S)
findTitle = re.compile(r'<div class="product__title">(.*?)</div>', re.S)  # 匹配标题
findQa = re.compile(r'class="product__sponsored-ad-label">.*(.*?).*</div>', re.S)  # 页面排名
findID = re.compile(r'/product/(\d*)/', re.S)  # kaufland专用id
findSeller = re.compile(r'(.*?) ', re.S)  # 竞卖
findSKU = re.compile(r'.* (.*?)$', re.S)  # SKU
findCategory = re.compile(r'<a.*data-category-name="(.*?)"')  # kaufland内置类目
findComment = re.compile(r'class="product-rating__count">\n        (\d*)\n', re.S)  # 评价数
kauf_id = 333735622


def get_inventory(kauf_id):
    doc = requests.get("https://www.kaufland.de/product/%d/" % kauf_id).text
    # print(doc)
    soup = str(BeautifulSoup(doc, "lxml"))
    inventory: list[Any] = re.findall(find_inventory, soup)
    print(inventory)
    inventory = inventory[-1]
    print(inventory)
    return inventory

# num = get_inventory(kauf_id)
def get_url(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(markup=html, features="lxml")
    return soup

link = "https://www.kaufland.de/item/search/?original_search_value=trampoline&search_value=trampolin"
datalist = []

def getData(link):
    i, b = 0, 0
    leixing = ""
    for a in range(1, 2):  # 开始循环，从第几页到第几页
        if leixing == "ProductList":
            url = link + "p" + str(a) + "/"  # 网址
        else:
            url = link + "&page=" + str(a)
        print(url)
        head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/93.0.4577.63 Safari/537.36 "
        }
        html = requests.get(url=url, headers=head).text  # 启动定义好的askurl程序，url在上边设定好了
        bs = BeautifulSoup(html, features="lxml")  # 解析网页，将html文件变成txt
        items = bs.find_all('article')  # 找到所有<article>，锁定
        for item in items:  # 在所有article中循环每一个article
            i += 1  # 每次循环+1
            print("第%s条" % i)
            # print(item)
            data = [str(datetime.date.today())]  # 清空data，重新循环
            item = str(item)  # 把item从集合中的元素转化为字符串
            # print(item)
            # 逐个解析

            title = re.findall(findTitle, item)
            # print(title)
            title = title[0]
            title = title.strip()  # 去掉前后的空格
            # print(title)

            seller = re.findall(findSeller, title)[0]
            sku = re.findall(findSKU, title)[0]
            # print(seller)
            # if seller not in ["VASAGLE", "SONGMICS", "FEANDREA"]:
            #     continue

            # data.append(suche)
            data.append(leixing)

            if seller in ['VASAGLE', 'SONGMICS', 'FEANDREA']:
                data.append(seller)
                data.append(sku)
            elif seller in ['Vicco', 'VICCO', 'SoBuy®', 'WOLTU', 'vidaXL', 'HOMEXPERTS']:
                data.append(seller)
                data.append("")
            else:
                data.append("")
                data.append("")

            data.append(title)

            try:
                productid = re.findall(findID, item)
                # print(id)
                data.append(productid[0])
                data.append(get_inventory(productid))
            except Exception:
                data.append("")
                data.append("")

            qa = re.findall(findQa, item)  # 根据上边写的正则表达式，在item中进行匹配，获得的是一个列表
            # print(qa)
            try:
                # qa = int(qa[0])
                qa = qa[0]
                data.append(qa)  # 取所有找到的qa中的第一个
                print(qa)
                data.append("sor")
            except IndexError:
                b += 1
                data.append(b)
                data.append("")
                print(item)

            comment = re.findall(findComment, item)
            try:
                data.append(int(comment[0]))
            except IndexError:
                data.append("")

            print(data)  # 看看每一个item中得到的data有没有错误
            # 添加数据
            datalist.append(data)  # 把data添加到datalist中，然后开始下次循环

    # print(datalist)
    return datalist  # 获得datalist

getData(link)
print(datalist)

'''
soup = get_url(url=link)
items = soup.find_all('article')
i = 0
for item in items:
    i += 1  # 每次循环+1
    print("第%s条" % i)
    item = str(item)

    title = re.findall(findTitle, item)[0].strip()
    print(title)

    seller = re.findall(findSeller, title)[0]
    sku = re.findall(findSKU, title)[0]

    print(seller, sku)
    # print(item)
    
'''

