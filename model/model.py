'''
@author ldc

'''
from utils.dbUtil import RedisUtil, MySQLUtil

# 用户模型类
class User:
	def __init__(self,username,password):
		self.username = username
		self.password = password

# UserDao
# 封装了对User数据的增删改查
# Dao=Database Access Object 数据库访问对象
class UserDao:
	# 创建数据库对象
	redis = RedisUtil()
	mySQL = MySQLUtil('homework','t_usr')

	# 执行数据库查询操作，返回查询结果
	@classmethod
	def query(cls,user,dbType):
		dataDict = {}
		dataDict["username"] = user.username
		dataDict["password"] = user.password
		if dbType == 'redis':
			return cls.redis.get(user.username)
		elif dbType == 'mysql':
			return cls.mySQL.query(dataDict)

	# 执行数据库查询操作，查询用户是否存在，返回查询结果
	@classmethod
	def exists(cls,username,dbType):
		dataDict = {}
		dataDict["username"] = username
		if dbType == 'redis':
			return cls.redis.exists(username)
		elif dbType == 'mysql':
			return cls.mySQL.exists(dataDict)
		else:
			pass

	# 执行数据插入操作，先把用户信息添加进mysql，然后再添加进redis
	@classmethod
	def insert(cls, user):
		dataDict = {}
		dataDict["username"] = user.username
		dataDict["password"] = user.password
		if cls.mySQL.insert(dataDict):
			cls.redis.set(user.username,user.password)
			return 1
		else:
			print("注册失败，服务器繁忙!!!")
			return 0

	# 修改密码
	@classmethod
	def changePasswd(cls, user):
		dataDict = {'changeCol': 'password = %s'%user.password, 'caluse' : 'username = %s'%user.username}
		if cls.mySQL.update(dataDict):
			cls.redis.set(user.username,user.password)
			return 1
		else:
			print("修改密码失败，服务器繁忙!!!")
			return 0

	# 注销用户
	@classmethod
	def deleteUser(cls, user):
		dataDict = {'username' : user.username}
		if cls.mySQL.delete(dataDict):
			cls.redis.delete(user.username)
			return 1
		else:
			print("修改密码失败，服务器繁忙!!!")
			return 0



