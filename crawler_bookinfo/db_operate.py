#!/usr/bin/env python
# -*- coding:utf-8-*-

import MySQLdb
import sys


class Mysql(object):
    def __init__(self, url, user, code, db_name):
        print '开始连接数据库 '
        self.db = MySQLdb.connect(url, user, code, db_name)
        print "连接成功！"
        self.cur = self.db.cursor()     # 获取游标对象
        print self.cur

    def db_create_table(self):
        seq = "CREATE TABLE book_info(rank int(4) primary key, name varchar(500), writer varchar(500), " \
              "publisher VARCHAR(500), pub_time VARCHAR(32), comment VARCHAR(32), recommend VARCHAR(32), " \
              "now_price VARCHAR(32), discount VARCHAR(32), pre_price VARCHAR(32))"
        self.cur.execute(seq)
        print '成功创建数据库'

    def db_load_book_info(self, file_name):
        fp = open(file_name)
        iter_fp = iter(fp)
        for line in fp:
            rank, name, writer, publisher, pub_time, comment, recommend, now_price, discount, pre_price =\
                    line.split('\t')
#            print rank, name, writer, publisher, pub_time, comment, recommend, now_price, discount, pre_price
            seq = "insert into book_info(rank, name, writer, publisher, pub_time, comment, recommend, now_price, " \
                  "discount, pre_price) values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                  % (int(rank), name, writer, publisher, pub_time, comment, recommend, now_price, discount, pre_price)
            self.cur.execute(seq)
        print'加载数据完成'

    def db_show(self):
        seq = 'select * from book_info'
        self.cur.execute(seq)
        result = self.cur.fetchall()    # 获取数据库的表单数据
        for info in result:             # 表单里的每个info 在这里是元组类型
            for item in info:           # 将元组里的每个元素单独打印出来
                print item

    def db_del(self):
        seq = 'DROP TABLE book_info'
        self.cur.execute(seq)
        print '清空数据库'

    def db_update(self):
        pass

    def db_inser(self):
        data_input = raw_input("Enter your insert:\nThe format(rank, name, writer, publisher, pub_time, comment, "
                               "recommend, now_price, discount, pre_price) \n>").strip()
        rank, name, writer, publisher, pub_time, comment, recommend, now_price, discount, pre_price = \
            data_input.split(',')

        seq = "insert into book_info(rank, name, writer, publisher, pub_time, comment, recommend, now_price, " \
              "discount, pre_price) values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
              % (int(rank), name, writer, publisher, pub_time, comment, recommend, now_price, discount, pre_price)
        self.cur.execute(seq)
        print seq

    def db_close(self):
        self.cur.close()
        self.db.commit()
        self.db.close()

    def db_display(self):
        while True:
            print """
            +++++++++++++++++++++++++++++++
            Enter your choice:
            1.show all the data
            2.insert data
            3.update data
            4.delete data
            5.delete table and quit....
            """
            cho = raw_input('>')
            if cho in ('1', '2', '3', '4', '5'):
                if cho == '1':
                    sql.db_show()
                elif cho == '2':
                    sql.db_inser()
                elif cho == '3':
                    sql.db_update()
                elif cho == '4':
                    sql.db_del()
                else:
                    print 'quit and shutdown....'
                    break
            else:
                print 'Enter Error, try again.'

if __name__ == '__main__':
    sql = Mysql('localhost', 'root', '123456', 'testdb')
    try:
        sql.db_del()
    except:
        pass
    sql.db_create_table()
    sql.db_load_book_info(sys.argv[1])
    sql.db_display()

