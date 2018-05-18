'''
@author ldc

'''
import os
import pymysql


'''
初始化服务：
1、在mysql上新建一个数据库“homework”和建表"t_usr"
2、开启redis服务程序
'''
# 建立数据库连接
conn = pymysql.connect(
	host='localhost',
	user='root',
	password="123456",
	port=3306
)
# 获取游标
cursor = conn.cursor()

# 创建数据库
dbname = 'homework'
sql='''
		create database if not EXISTS %s charset=utf8;
    '''%dbname

cursor.execute(sql)
# 使用数据库
cursor.execute('use %s'%dbname)
# 创建表
sql = '''
	 create table if not EXISTS t_usr(
          id INTEGER PRIMARY KEY auto_increment,
          username varchar(20) unique not null,
          password varchar(20) not null
        );
'''
cursor.execute(sql)
# 关闭游标与连接
cursor.close()
conn.close()

# 开启redis服务，新建一个启动redisd.bat文件，以后开启redis服务就可以直接打开这个文件了
def openRedisd(path):
	rPath = """@echo off
				redis-server %s
				pause"""%path
	with open(r"C:\Users\LDCPC\Desktop\启动redisd.bat","w",encoding="ANSI") as f:
		f.write(rPath)

openRedisd(r"D:\ruanjian\redis-64.2.8.2101\redis.windows.conf")
# 打开文件“启动redisd.bat”
os.popen(r"C:\Users\LDCPC\Desktop\启动redisd.bat")
