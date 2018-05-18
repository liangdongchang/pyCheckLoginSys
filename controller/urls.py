'''
@author ldc

'''
from model.model import UserDao

# 先查询该用户是否存在数据库中
def exists(user):
	'''先查看Redis缓存中是否有该用户数据'''
	if not UserDao.exists(user.username, 'redis'):
		'''然后在mysql中查询该用户是否存在'''
		if UserDao.exists(user.username, 'mysql'):
			# 若在mysql存在就把该用户写进redis,
			UserDao.redis.set(user.username, user.password)
			return 'mysql'
		else :
			return None
	return 'redis'

'''
# 登录模块
先在redis上验证，验证成功则提示在redis上验证成功
否则到mysql中验证，验证成功则提示在mysql上验证成功
否则提示用户不存在
'''
def login(user):
	print("------------登录界面------------")
	# 查询该用户信息是否存在数据库中
	whereDB = exists(user)
	if whereDB == 'redis':
		# 匹配密码是否正确
		if UserDao.query(user, 'redis') == user.password:
			print("[在redis中查询到该用户]登录成功!!!")
			return 1
		else:
			print("[在redis中查询到该用户] 登录失败,用户名或者密码不正确!!!")
	elif whereDB == 'mysql':
		# 匹配密码是否正确
		if UserDao.query(user, 'mysql'):
			print("[在mysql中查询到该用户] 登录成功!!!")
			return 1
		else:
			print("[在mysql中查询到该用户] 登录失败,用户或者密码不正确!!!")
	else:
		print("[在mysql中查询不到该用户] 登录失败,该用户不存在，请注册后再登录!!!")
	return 0

'''
# 注册模块
先在redis上查询账号是否存在，存在则注册失败
否则到mysql上查询，用户存在则注册失败
否则注册成功，把账号写进mysql，写进redis
'''
def regist(user):
	print("------------注册界面------------")
	# 查询该用户信息是否存在数据库中
	whereDB = exists(user)
	if whereDB :
		print("注册失败，该用户已存在!!!")
	else:
		if UserDao.insert(user):
			print("注册成功!!!")
		else:
			print("注册失败!!!")
'''
# 修改密码模块
先在redis上和mysql上查询，用户存在就在mysql上修改该用户密码，然后把该用户信息重新写进redis中
在mysql中查询不到该用户，就返回该用户不存在，改密失败
'''

def changePasswd(user):
	print("------------改密界面------------")
	# 查询该用户信息是否存在数据库中
	whereDB = exists(user)
	if whereDB:
		user.password = input("请输入新密码：")
		if UserDao.changePasswd(user):
			print("改密成功!!!")
		else:
			print("改密失败!!!")
	else:
		print("用户不存在，改密失败!!!")

'''
# 注销用户模块
先在在redis上和mysql上查询，用户存在就在mysql和redis上删除该用户
在mysql中查询不到该用户，就返回该用户不存在，注销失败
'''

def deleteUser(user):
	print("------------注销界面------------")
	# 查询该用户信息是否存在数据库中

	if login(user):
		if UserDao.deleteUser(user):
			print("注销成功!!!")
			return
	print("注销失败!!!")
