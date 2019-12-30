import requests
import ssl
import re
import time
ssl._create_default_https_context = ssl._create_unverified_context
session = requests.session()
#requestsSession = requests.Session()                                # 开启会话
requestsAdapterA = requests.adapters.HTTPAdapter(max_retries=3)     # 挂载适配器
session.mount('http://', requestsAdapterA)
session.mount('https://', requestsAdapterA)   



#爬取关注的函数：id 传入的是数组，turn传入的是层数
#按照优先级"个>层>递归"，就是先第0层第一个：[]，第0层第二个：[]......  然后把一层弄完，然后递归，然后再找第1层的第一个。
def follow_spider(id_all,turn):
	#控制迭代次数
	if(turn == 2):
		print('\n'+"已经达到需要爬取的层数，准备退出......")
		exit()
	else:
		#最外层的for，是用来循环这一层函数中id_all的值
		print('第'+str(turn)+'层开始：'+'\n'+'该层需要爬取的id有：')
		print(id_all)
		uid_all=[]
		
		for id in id_all:
			people=0
			time.sleep(5)
			#登录以后使用新的headers
			headers_logined={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
			
			#先标记名字id
			url_for_name='https://weibo.cn/'+id
			try:
				l=session.get(url=url_for_name,headers=headers_logined,timeout=3)
				name=re.findall(r'<title>(.*?)的微博</title>',l.text)
				print('\n'+'开始爬取'+id+'||'+name[0]+'的所有关注\n')
			except:
				continue
			follow_url= 'https://weibo.cn/'+str(id)+'/follow'
			login=session.get(url=follow_url,headers=headers_logined,timeout=3)
			pages = re.findall(r'value="跳页" />&nbsp;1\/(.*?)页',login.text)
			#print(pages)
			if len(pages)==0:
				print('\n'+"只有一页，以下是"+id+'||'+name[0]+'的所有关注')
				page_all=['0']
			else:
				page_all=str(pages[0])
			follow_all=[]
			uid_part=[]
			print(page_all)
			
			if(page_all[0]=="0"):
				follow_url = 'https://weibo.cn/'+str(id)+'/follow'
				login=session.get(url=follow_url,headers=headers_logined,timeout=3)
				follow_part=re.findall(r'<td valign="top"><a.*?href="(.*?)">(.*?)</a>',login.text)
				follow_all = follow_all+follow_part
			else:
				#循环取每一页的关注和他的主页，但是这里取不到id，所以还得继续根据主页取
				
				for page in range(int(page_all)):
					page = page+1
					follow_url = 'https://weibo.cn/'+str(id)+'/follow?page=' + str(page)
					login=session.get(url=follow_url,headers=headers_logined,timeout=3)
					#匹配出来结果为关注的用户名昵称，是个二重数组，list里面再有一个list，follow_part[1][0]取主页url，follower[1][1]来取用户名
					follow_part=re.findall(r'<td valign="top"><a.*?href="(.*?)">(.*?)</a>',login.text)
					follow_all = follow_all+follow_part
					time.sleep(3)
			#当关注数量大于150个的时候，跳过不计算
			#follow_all为所有关注及其对应的主页
			print(follow_all)
			#根据主页取每一个关注的id，凑成uid_all
			name_list=[]
			for s in range(len(follow_all)):
				if("微博" in follow_all[s][1]):
					continue
				follower=session.get(follow_all[s][0],headers=headers_logined,timeout=3)
				uid = re.findall(r'私信</a>&nbsp;<a href="/(.*?)/info">资料</a>',follower.text)
				print(str(s) +'  '+ follow_all[s][1] + ': ')
				print(uid)
				#这是某一个的总集合
				uid_part = uid_part + uid
				name_list.append(follow_all[s][1])
				#people=people+1
				#if(people>50):
				#	print("已经爬取前50个关注")
				#	break
				time.sleep(1.5)
			print('\n'+'这是'+id+'__'+name[0]+'的所有关注')
			#写入每个文件的一定要是用户名，才好做数据对齐
			print(name_list)
			file_name=name[0]+'.txt'
			with open('./weibo/'+file_name,'w',encoding="utf-8") as f:
				f.write(str(name_list))
			
			
			#for one in uid_part:
			#	url_one='https://weibo.cn/'+one
			#	l=session.get(url=url_one,headers=headers_logined)
			#	name_one=re.findall(r'<title>(.*?)的微博</title>',l.text)
			#	name_list = name_list+name_one
			
			print('\n该用户的关注名单已经写入文件\n')
			
			#这层的某一个算完以后加入这一层的总集合)
			uid_all=uid_part+uid_all
		#print('第'+str(turn)+'层得到的结果：')
		#print(uid_all)
		#最外层循环结束
		print('\n'+'第'+str(turn)+'层结束：')
	turn = turn +1
	follow_spider(uid_all,turn)

if __name__ == '__main__':
	#注意微博登录时候不能加proxies，会报错，系统错误
	url='https://passport.weibo.cn/sso/login'
	headers={
	'Host': 'passport.weibo.cn',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
	'Accept': '*/*',
	'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': 'https://passport.weibo.cn',
	'Connection': 'close',
	'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=',
	'Cookie': '_T_WM=8d0aa03340d64b0e619bac816df51e1c; login=d434df472bb5ab59af1d4577b2b5d916'
	}
	data={
		     'username': '17538142787',
	            'password': 'Zzh331759019',
	            'savestate': '1',
	            'r': '',
	            'ec': '0',
	            'pagerefer': 'http://weibo.cn/',
	            'entry': 'mweibo',
	            'wentry': '',
	            'loginfrom': '',
	            'client_id': '',
	            'code': '',
	            'qq': '',
	            'mainpageflag': '1',
	            'hff': '',
	            'hfp': '',
	}
	login=session.post(url=url,headers=headers,data=data)
	if("20000000" not in login.text):
		print("登陆失败")
		exit()
	login.encoding='utf-8'

	#定义开始爬取的种子
	#urls = 'https://weibo.cn/1234552257/follow'
	follow_spider(['1774978073','1223178222'],0)