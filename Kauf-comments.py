# -*- coding = utf-8 -*-
# @Time : 2021-10-22 18:45
# @Author : 帅哥张
# @File : Kauf-comments.py
# @Software: PyCharm
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
import xlwt
import datetime
import time
'''
class kauf_comments_all(object):

    def __init__(self, filename):
        self._filename = filename
        datalist = []
        savepath = "KAUF-comments-%s" % datetime.date.today()

    def get_url(self, url):
        doc = requests.get(url=url).json()
        totalreviews = doc['totalReviews']
        averageRating = doc['averageRating']
        print(totalreviews, averageRating)
        reviews = doc['reviews']
        return reviews

    def get_data(self, reviews):
        for items in reviews:
            i += 1
            data = []
            print("第 %s 项" % i)
            print(items)
            reviewId = items['reviewId']
            title = items['title']
            title = title.strip()
            date = items['date']
            rating = items['rating']
            isVerifiedPurchase = items['isVerifiedPurchase']
            text = items['text']
            text = re.sub("<br />", "", text)
            text = text.strip()
            author = items['author']
            datePublished = items['datePublished']
            data.append(reviewId)
            data.append(date)
            data.append(datePublished)
            data.append(rating)
            data.append(isVerifiedPurchase)
            data.append(title)
            data.append(text)
            data.append(author)
            for item in items['variantAttributes']:
                print(item)
                data.append(item['title'])
                data.append(item['label'])

    def save_data(self, ):

    def main(self):
        for listing in list(pd.read_excel(self._filename).loc[:, "ProductID"]):
            get_url
'''

i = 0
file = pd.read_excel("kauf_id.xlsx")
id_items = list(file.loc[:, "id_item"])
ean_list = list(file.loc[:, 'ean'])
print(ean_list)
id_items = ['429768195', '333190854']
print(len(id_items))
datalist = []

for id_item in id_items:
    try:
        print(id_item)
        html_id = "https://www.kaufland.de/backend/product-detail-page/v1/%s/product-reviews/?offset=0&limit=2000" % id_item
        print(html_id)
        html = requests.get(html_id)
        doc = html.json()
        print(doc)
        if doc['totalReviews']:
            totalreviews = doc['totalReviews']
        else:
            totalreviews = ''
        if doc['averageRating']:
            averageRating = doc['averageRating']
        else:
            averageRating = ''

        reviews = doc['reviews']
        print(reviews)

        for items in reviews:
            i += 1
            data = []
            print("第 %s 项" % i)
            print(items)
            reviewId = items['reviewId']

            title = items['title']
            title = title.strip()
            date = items['date']
            rating = items['rating']
            isVerifiedPurchase = items['isVerifiedPurchase']
            text = items['text']
            text = re.sub("<br />","",text)
            text = text.strip()
            author = items['author']
            datePublished = items['datePublished']
            data.append(id_item)
            data.append(totalreviews)
            data.append(averageRating)
            data.append(reviewId)
            data.append(date)
            data.append(datePublished)
            data.append(rating)
            data.append(isVerifiedPurchase)
            data.append(title)
            data.append(text)
            data.append(author)
            for item in items['variantAttributes']:
                print(item)
                data.append(item['title'])
                data.append(item['label'])

            datalist.append(data)
    except Exception:
        continue

titlestyle = xlwt.XFStyle()
font = xlwt.Font()
font.name = "Calibri"
font.bold = True
font.height = 12 * 30  #
font.colour_index = 0x09

pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设定为单元格有填充颜色
pattern.pattern_fore_colour = 0x0A  # 设定填充颜色
# pattern.pattern_back_colour = 0x1E #似乎无用

titlestyle.pattern = pattern
titlestyle.font = font


book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
sheet = book.add_sheet('zhang', cell_overwrite_ok=True)  # 创建工作表
col = ("id", "totalReviews", "averageRating", "date", "datePublished", "rating", "isVerifiedPurchase", "title", "text", "author", "label")
for i in range(0, len(col)):
    sheet.write(0, i, col[i], titlestyle)  # 列名，其实就是写入第一行

for i in range(0, len(datalist)):  # 一层循环，从上往下循环一定行数
    print("第%d条" % (i + 1))
    data = datalist[i]
    for j in range(0, len(data)):  # 二层循环，在每一行循环一定列数
        sheet.write(i + 1, j, data[j])  # 数据


savepath = f"Kaufland-{datetime.date.today()}.xls"
book.save(savepath)  # 保存
print("文件保存完毕")
