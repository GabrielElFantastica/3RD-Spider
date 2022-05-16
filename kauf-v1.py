# -*- coding = utf-8 -*-
# @Time : 2021-09-07 16:51
# @Author : 帅哥张
# @File : kauf-v1.py
# @Software: PyCharm

#引入代码包，也就是前人写好的代码段，用ctrl点击可以查看
from bs4 import BeautifulSoup #解析网页返回的html文件的包
import re #使用正则表达式的包
import xlwt #使用excel的包
import urllib.request, urllib.error #发送网页请求的包
import time

Deutsch = "Badezimmerschraenke" #定义一个命名文件用的变量

def main(): #定义主程序
    baseurl = "https://www.kaufland.de/badezimmerschraenke/p" #目标网址
    datalist = getData(baseurl) #根据baseurl获取并解析数据，缓存起来，命名为datalist
    savepath = "KAUF-%s.xls" % Deutsch #使用%s做占位字符串，外边%Deutsch，即为把Deutsch这个变量以字符串的形式写入引号中
    saveData(datalist, savepath) #把手机号的datalist存到savepath中


#正则表达式，用于定义所需字符串在页面html文件中的位置，具体可使用网页版的开发者工具进行查看
# findLink = re.compile(r'<a.*href="(.*?)".*>')
findTitle = re.compile(r'<div class="product__title">(.*?)</div>', re.S)  # 匹配标题
findPrice = re.compile(r'<a.*data-price="(.*?)"', re.S)  # 价格
findQa = re.compile(r'<a.*tabindex="(\d*)"', re.S)  # 页面排名
findImg = re.compile(r'<img.*class=".*src="(.*?)"')  # 图片链接
findID = re.compile(r'href="/product/(\d*)/"', re.S)  # kaufland专用id
findSeller = re.compile(r'<a.*data-brand-name="(.*?)"', re.S)  # 竞卖
findStar = re.compile(r'fill="(.*?)"', re.S)  # 星级，以色块集合的形式展现
findComment = re.compile(r'class="product-rating__count">\n        (\d*)\n', re.S)  # 评价数
findCategory = re.compile(r'<a.*data-category-name="(.*?)"')  # kaufland内置类目
findUvp = re.compile(r'<div.*class="price__old price__old--uvp">(.*?)</div>', re.S)  # 划线价
findsaving = re.compile(r'<div.*class="price__savings">(.*?)</div>', re.S)  # 旁边显示的折扣
findBestseller = re.compile(r'<div.*class="badge badge--blue">(.*?)</div>', re.S)  # Bestseller标记，据说没啥用

# print(bs.article.contents)    #打印第一个article的所有内容

#对获取到的html文件进行解析的程序
def getData(baseurl):
    i = 0
    b = 0
    datalist = []
    for a in range(1, 20):#开始循环，从第几页到第几页
        url = baseurl + str(a) #网址
        print(url)
        html = askURL(url) #启动定义好的askurl程序，url在上边设定好了
        bs = BeautifulSoup(html, "lxml") #解析网页，将html文件变成txt
        items = bs.find_all('article') #找到所有<article>，锁定
        for item in items: #在所有article中循环每一个article
            i += 1 #每次循环+1
            print("第%s条" % i)
            # print(item)
            data = [] #清空data，重新循环
            item = str(item) #把item从集合中的元素转化为字符串
            print(item)
            #逐个解析
            qa = re.findall(findQa, item) #根据上边写的正则表达式，在item中进行匹配，获得的是一个列表
            print(qa)
            try:
                qa = int(qa[0])
                data.append(qa) #取所有找到的qa中的第一个
            except IndexError:
                b += 1
                data.append(b)

            data.append("") #人为空一列

            seller = re.findall(findSeller, item)
            data.append(seller)

            bestseller = re.findall(findBestseller, item)
            if bestseller != []:
                bestseller = bestseller[0]
                bestseller = bestseller.strip() #去掉首尾空格
                data.append(bestseller)
            else:
                data.append("")

            category = re.findall(findCategory, item)
            data.append(category)
            #
            title = re.findall(findTitle, item)
            title = title[0]
            title = title.strip() # 去掉前后的空格
            data.append(title)
            #
            price = re.findall(findPrice, item)
            data.append(price)

            uvp = re.findall(findUvp, item)
            # print(uvp)
            if uvp != []:
                uvp = uvp[0]
                uvp = uvp.strip()
                data.append(uvp)
            else:
                data.append("")

            saving = re.findall(findsaving, item)
            if saving != []:
                saving = saving[0]
                saving = saving.strip()
                data.append(saving)
            else:
                data.append("")

            id = re.findall(findID, item)
            # print(id)
            data.append(id)

            star = re.findall(findStar, item)

            data.append(star)

            comment = re.findall(findComment, item)
            print(comment)
            data.append(comment)

            imglink = re.findall(findImg, item)[0]
            data.append('<table><tr><td><img src=\"%s\" width=\"100\" height=\"100\"/></td></tr></table>' % imglink) #把拿到的图片链接跟已有字符串组合一下

            # link = re.findall(findLink,item)
            # if link != []:
            #     link = link[0]
            #     data.append("https://www.kaufland.de%s"%link)
            # else:
            #     data.append("")
            if id == []:
                data.append("")
            else:
                data.append("https://www.kaufland.de/product/%s/" % id[0]) #Kaufland独有lisitng链接组合方式


            print(data) #看看每一个item中得到的data有没有错误
            #添加数据
            datalist.append(data) #把data添加到datalist中，然后开始下次循环

    # print(datalist)
    return datalist #获得datalist

head = {        #模拟浏览器头部信息，向服务器发送消息
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
#用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是我的网络身份证），每人每个浏览器都不一样

def askURL(url): #获取网页内容的程序，在getData程序中调用
    request = urllib.request.Request(url, headers=head) #根据设定好的headers发起请求，
    html = ""
    try:
        response = urllib.request.urlopen(request) #将收到的文件命名为response
        html = response.read().decode("utf-8") #用可以编译中文的编码编译response，得到文件，命名为html
        # print(html)
    except urllib.error.URLError as e: #iferror，汇报原因
        if hasattr(e, "code"): #错误代码
            print(e.code)
        if hasattr(e, "reason"): #错误原因
            print(e.reason)
    return html #获得html


bodystyle = xlwt.XFStyle()
font = xlwt.Font()
bodystyle.name = 'Calibri'
bodystyle.font = font

def saveData(datalist,savepath): ##定义存储方法的程序
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('HandsomeZhang', cell_overwrite_ok=True)    #创建工作表
    col = ("排名", "图片", "卖家", "Bestseller", "DE类目", "标题", "价格", "UVP价格", "折扣", "ID", "星级", "评价数", "图片链接", "listing链接")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i], titlestyle()) #列名
    for i in range(0, len(datalist)): #一层循环，从上往下循环一定行数
        # print("第%d条" % (i+1))
        data = datalist[i]
        # style_body = xlwt.easyxf('font:height 1000;')
        # style = style_body
        # sheet.row(i +1).set_style(style)

        for j in range(0, len(data)): ##二层循环，在每一行循环一定列数

            sheet.write(i+1, j, data[j], bodystyle)      #数据

    book.save(savepath)       #保存
    print("文件保存完毕")

def titlestyle(): #定义excel标题格式
    titlestyle = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "Calibri"
    font.bold = True
    font.height = 12*25 #前一个数字是字号，后一个类似于列宽
    font.colour_index = 0x09

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN #不太理解为啥需要这句话
    pattern.pattern_fore_colour = 0x0A #红色的颜色码，具体参照colourmap
    # pattern.pattern_back_colour = 0x1E #似乎无用

    titlestyle.pattern = pattern
    titlestyle.font = font

    return titlestyle


if __name__ == "__main__":    #运行主程序
    start = time.localtime()
    main()
    print("爬取完毕")
    end = time.localtime()
    print("开始时间：%s" % (time.strftime("%Y-%m-%d %H:%M:%S", start)))
    print("结束时间：%s" % (time.strftime("%Y-%m-%d %H:%M:%S", end)))