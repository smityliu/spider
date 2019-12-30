import requests
import ssl
import re
import json
ssl._create_default_https_context = ssl._create_unverified_context
session = requests.session()

#使用前务必填写你的authorization

def spider_follower(id_all,name_all,turn):
	print("这是第"+str(turn)+"层：")
	print(id_all)
	print(name_all)
	if(turn == 3):
		print("达到层数，退出")
		exit()
	headers_json={
	
	'authorization': '请填写你自己账户的authorization',
	
	'content-type': 'application/x-www-form-urlencoded',
	'Origin': 'https://twitter.com',
	'Sec-Fetch-Mode': 'cors',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
	#建议每次用脚本之前，都去浏览器再重新更新一下cookie，以防过期，获取过程很简单，直接看发包就可以了，然后整个脱下来。
	'Cookie':'_ga=GA1.2.175021092.1575685463; kdt=lrXc3mPTTmt2DGsT6bCTvOV9g4ALcrWad2uxcrL8; remember_checked_on=1; csrf_same_site_set=1; csrf_same_site=1; personalization_id="v1_l2QIehqV66tm00Fqv1KWjg=="; guest_id=v1%3A157591105501143280; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCFTKcjNvAToMY3NyZl9p%250AZCIlODA0NDc2ZjQ2NjFjNjIyMjIxN2E2ODYyNGFlZDIwMzg6B2lkIiUzMzA2%250AZjFlNmRjYWJlZDY5N2Q4NmExZTVjMjcwNjgzYjoJdXNlcmwrCQBQ1M2lZrIQ--88ffc80488d04b385eb14dfb4d99fd3a73afc5cd; ct0=97e791a574a3a81468622aefcee61068; _gid=GA1.2.1844811109.1577116163; ads_prefs="HBERAAA="; twid=u%3D1203136912770224128; auth_token=ee2e68cb2272ee1e86318690e5874212cafea487; rweb_optin=side_no_out',
	'x-csrf-token':'97e791a574a3a81468622aefcee61068'}
	position=0
	id_next_all=[]
	follower_name_all=[]
	for ids in id_all:
		url='https://api.twitter.com/1.1/friends/list.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cursor=-1&user_id='+str(ids)+'&count=100'
		follower = session.get(url=url,headers=headers_json,proxies=proxies)
		follower_json=json.loads(follower.text)
		#print(follower_json)
		follower_name=[]
		id_next=[]
		#这个follower是json格式了已经，follower_json["users"]还是一个list
		for follower in follower_json["users"]:
			#print("screen_name: "+follower["screen_name"])
			id_next.append(follower["id_str"])
			follower_name.append(follower["name"])
		print('\n')
		print(ids)
		str(name_all[position]).replace(' ','_').replace('?','_').replace('.','_').replace('/','_').replace('\\','_').replace('"','_').replace('<','_').replace('>','_').replace('|','_').replace('\'','_')
		filename=str(name_all[position])+'.txt'
		print(filename)
		print('\n')
		try:
			with open('./twitter/'+filename,'w',encoding='utf-8') as f:
				f.write(str(follower_name))
		except:
			pass
		position=position+1
		id_next_all=id_next_all+id_next
		follower_name_all = follower_name_all + follower_name
	turn = turn +1
	print(id_next_all)
	print(follower_name_all)
	spider_follower(id_next_all,follower_name_all,turn)
		
if __name__ == '__main__':
	#这一步是先访问twitter主页面获取authenticity_token，后面登录要用
	url="https://twitter.com"
	proxies={'https':'127.0.0.1:10809','http':'127.0.0.1:10809'}
	headers={
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Origin': 'https://twitter.com',
				'Referer': 'https://twitter.com/login'
			  }

	login=session.get(url=url,proxies=proxies)
	if("authenticity_token" in login.text):
		pattern=re.compile(r'<input type="hidden" value="(.*?)" name="authenticity_token">')
		m=re.findall(pattern,login.text)
		print(m[0])
		data={
				#填自己用户名密码
				'session[username_or_email]':'***********'
	             	      'session[password]':'**********',
	                   'return_to_ssl':'true',
	                   'scribe_log':'',
	                   'redirect_after_login':'/',
	                   'authenticity_token':m[0]
		}
		print(data)
		
		#这一步是在已经成功获取authenticity_token的基础上，做模拟登录
		url='https://twitter.com/sessions'
		login=session.post(url=url,headers=headers,data=data,proxies=proxies)
		#print(login.headers)
		#如果没有登录成功，会返回一堆html，里面有log in字样，如果成功了则返回的html很短，并且content的内容是herf=什么什么的

	#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----------------#----
		#这一步是爬取用户的关注列表，其实不模拟登录也是可以的，模拟登录只是为了让你获取到你的authorization，这个地方构造请求很复杂，因为他是调用了api，一定要满足请求规则：1. 有csrf_token. 2. 有authorization
		#authorization每个账户都是唯一的，x-csrf-token这个就是Cookie中的ct0参数，这里有一个安全漏洞，就是你的Cookie可以自己构造，直接拿一个浏览器访问的cookie去做就ok了，他也不会去校验到底这个ct0的值是不是最新的。
		#http://gettwitterid.com/?user_name=TheTweetOfGod&submit=GET+USER+ID，这个可以查user_id
		#这里的userid就是你要爬取的用户的，count记录的时爬取的关注个数，范围太大就返回全部
		id_all=['83570815','943048100','1059194370']
		name_all=['Stefsunyanzi','DonnieYenCT','kobebryant']
		spider_follower(id_all,name_all,0)