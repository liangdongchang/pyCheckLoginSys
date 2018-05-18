'''
@author ldc

'''
import pymysql
import redis as redis

'''
MySQL增删改查操作类
'''
class MySQLUtil:
	def __init__(self,dbName,tableName):
		self.dbName = dbName
		self.tableName = tableName

	# 连接数据库,并生成全局可用的连接对象和查询游标
	def connect(self):
		self.conn = pymysql.connect(
			host='localhost', user='root', password="123456",
			database=self.dbName, port=3306,
		)
		self.cursor = self.conn.cursor()

	# 关闭全局游标，断开全局连接
	def disconnect(self):
		self.cursor.close()
		self.conn.close()

	# 查询用户名是否存在
	def exists(self,dataDict):
		caluse = ''
		for key,value in dataDict.items():
			caluse += key + '="'+ value + '"'
		# print(caluse)
		sql = """
				select * from %s where  %s ;
			  """ % (self.tableName, caluse)
		return self.execute(sql)
	# 验证用户名和密码是否正确
	def query(self, dataDict):
		# 查询子条件拼接
		caluse = ''
		for key, value in dataDict.items():
			caluse += key + '="' + value + '" and '
		caluse = caluse[:-4]
		# print(caluse)
		sql = """
				select * from %s where %s;
		      """% (self.tableName, caluse)
		return self.execute(sql)

	# 添加新用户
	def insert(self, dataDict):
		# sql语句拼接
		columns = ''
		values = ''
		for key, value in dataDict.items():
			columns += key + ','
			values += '"' + value + '",'
		columns = columns[:-1]
		values = values[:-1]
		sql = """
				insert into %s (%s) VALUES (%s);
			  """ % (self.tableName, columns,values)
		# print(sql)
		return self.execute(sql)

	# 更新
	def update(self, dataDict):
		# sql语句拼接
		changeCol = dataDict['changeCol']  #要改变值的列名
		caluse = dataDict['caluse']  #要改变值的子条件
		sql = 'update %s set %s where %s' %(self.tableName, changeCol, caluse)
		return self.execute(sql)

	# 删除
	def delete(self, dataDict):
		# sql语句拼接
		caluse = ''
		for key,value in dataDict.items():
			caluse += key + '="' + value + '"'

		sql = """
				delete from %s where %s;
			  """ % (self.tableName,caluse)
		# print(sql)
		return self.execute(sql)
	# print(sql)

	# 执行sql语句
	def execute(self, sql):
		self.connect()
		affected = 0
		try:
			affected = self.cursor.execute(sql)
		except BaseException as e:
			print(e)
			affected = 0
		finally:
			self.conn.commit()
			self.disconnect()
			return affected

'''
redis增删改查操作类
'''
class RedisUtil:
	# redis连接
	@classmethod
	def connect(cls):
		cls.client = redis.Redis(
			host='localhost', port=6379,
			db=1, password='123456',
		)

	# 判断键是否存在
	@classmethod
	def exists(cls,key):
		return cls.client.exists(key)

	# 存储键值,
	@classmethod
	def set(cls,key,value):
		# 键值存储在缓存中，保留时间为30秒
		cls.client.setex(key,value,30)

	# 获取键值
	@classmethod
	def get(cls,key):
		res = cls.client.get(key).decode("utf-8")
		return res
	# 删除键值
	def delete(cls, key):
		cls.client.delete(key)
