'''
@author ldc
'''
from controller import urls
from model.model import User
from utils.dbUtil import RedisUtil

'''
需求：登录注册验证
1、登录
2、注册
3、改密
4、注销
'''
# 主界面接口
def index():
	while True:
		#登录界面
		print("********************************")
		print("*                              *")
		print("*    (1) 登录      (2)注册     *")
		print("*    (3) 改密      (4)注销     *")
		print("*            (5)退出           *")
		print("********************************")
		print()
		num = input("请输入功能序号：")
		if num in ['1','2','3','4','5']:
			return num
		else:
			print("输入有误，请重新输入!!!")
# 输入账号与密码
def inputInfo():
	return input("请输入账号和密码(逗号隔开)：").split(',')


if __name__ == '__main__':
	# 连接redis数据库
	RedisUtil.connect()
	while True:
		# 初始化界面
		num = index()
		# 输入账号密码
		username, password = inputInfo()
		# 实例化一个用户类
		user = User(username, password)
		if num == '1':
			urls.login(user)  #登录
		elif num == '2':
			urls.regist(user)  # 注册
		elif num == '3':
			urls.changePasswd(user)  # 改密
		elif num == '4':
			urls.deleteUser(user)  # 注销
		else:
			break


