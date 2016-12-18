# -*- coding:utf-8 -*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# 以上三行，强制将命令提示行转换为utf-8


class BookSpider(object):
    def __init__(self, html):
        self.html = html
        print '开始爬取网页内容...'

    def rank_title(self):   # 爬取标题
        title = re.search("<title>(.*?)</title>", self.html.text).group(1)  # title
        title_2 = re.findall('<h1>(.*?)<span>(.*?)</span></h1>', self.html.text)  # title_2[0][1]
        return title + '\t' + title_2[0][1]

    def book_rank(self):    # 爬取排名
        book_rank = re.findall('<li>.*?<div class="number.*?>(\d+)</div>.*?<div class="pic"><a href=',
                               self.html.content, re.S)
        return book_rank

    def book_name(self):    # 爬取书名
        book_name = re.findall('target="_blank" title="(.*)">', self.html.text)
        return book_name

    def book_writer(self):   # 爬取作者
        book_writers = re.findall('\n .*?" title="(.*?)" target="_blank">.*?</a>', self.html.text)
        return book_writers

    def book_publish(self): # 爬取出版社
        book_publish = re.findall('<span>/</span><a href=.*target="_blank">(.*?)</a>', self.html.text)
        return book_publish

    def book_recommend(self):   # 爬取推荐指数
        book_recommend = re.findall('target="_blank">[0-9]+.*?</a><span .*?>(.*?)</span></div>', self.html.text)
        return book_recommend

    def book_estimate(self):    # 爬取评论条数
        book_estimate = re.findall('target="_blank">([0-9]+.*?)</a><span', self.html.text)
        return book_estimate

    def book_publ_time(self):   # 爬取出版时间
        book_pub_time = re.findall('<div class="publisher_info">.*?<span>(.*?)</span>', self.html.content, re.S)
        return book_pub_time

    def book_price(self):       # 爬取现价
        book_prices = re.findall('<p>.*?<span class="price_n">&yen;(.*?)</span>', self.html.text, re.S)
        return book_prices

    def book_discount(self):    # 爬取折扣
        book_discount = re.findall('<p>.*?"price_n">&yen;.*?"price_s">(.*?)</span>', self.html.text, re.S)
        return book_discount

    def book_origin_price(self):    # 爬取原价
        book_prices_origin = re.findall('<p>.*?price_n.*?"price_r">&yen;(.*?)</span>.*?price_s', self.html.text, re.S)
        return book_prices_origin

    # 保存爬取的数据到本地
    def book_info_save(self, title, book_rank, book_name, book_writer, book_publish, book_estimate,
                       book_recommend, book_publ_time, book_price, book_discount, book_origin_price):
        if book_rank[0] == '1':
            fp = open('bookinfo.txt', 'w')
        #   fp.writelines('\n' + title + '\t' + '\n\n')
        #   fp.writelines('排名\t\t详细信息' + '\n')
            fp.close()
        fp = open('bookinfo.txt', 'a+')
        for h1, h2, h3, h4, h5, h6, h7, h8, h9, h10 in zip(book_rank, book_name, book_writer, book_publish,
                                                           book_publ_time, book_estimate, book_recommend, book_price,
                                                           book_discount, book_origin_price):

            fp.writelines(h1 + '\t' + h2 + '\t作者：' + h3 + '\t出版社：' + h4 + '\t出版时间：' + h5 + '\t评价：' + h6 +
                          '\t推荐指数:' + h7 + '\t现价：' + h8 + '\t折扣：' + h9 + '\t原价：' + h10 + '\n')
        fp.close()


def main():
    i = 0
    while i < 25:   # 实现翻页
        i += 1
        print '正在处理页面: ', 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2015-0-2-%d' % i
        url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-2015-0-2-%d' % i  # 暴力翻页
        html = requests.get(url)
        print '连接状体：', html.status_code
        bs = BookSpider(html)
        title = bs.rank_title()
        book_rank = bs.book_rank()
        book_name = bs.book_name()
        book_writer = bs.book_writer()
        book_publish = bs.book_publish()
        book_estimate = bs.book_estimate()
        book_recommend = bs.book_recommend()
        book_publ_time = bs.book_publ_time()
        book_price = bs.book_price()
        book_discount = bs.book_discount()
        book_origin_price = bs.book_origin_price()

        bs.book_info_save(title, book_rank, book_name, book_writer, book_publish, book_estimate, book_recommend,
                          book_publ_time, book_price, book_discount, book_origin_price)
        print 'done !'

if __name__ == '__main__':
    main()
