import pymysql

conn = pymysql.connect(host="10.192.52.189", user="qql", password="123", database="haha", charset="utf8")
print(conn)
cur = conn.cursor()
cur.execute('drop table if exists user')
sql1 = """CREATE TABLE IF NOT EXISTS `user` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `name` varchar(255) NOT NULL,
	  `passwd` int(11) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
cur.execute(sql1)
sql = "insert into user values(2,'tom',18);"
insert = cur.execute(sql)
sql="insert into user values(%s,%s,%s)"
insert=cur.executemany(sql,[(4,'wen',20),(5,'tom',10),(6,'MainWindow',30)])
print('添加语句受影响的行数：',insert)
cur.connection.commit()
cur.close()
conn.close()

# print(type(conn))

