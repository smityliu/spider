import requests
import json
import re
#返回一个json，里面有min-position
#https://twitter.com/i/profiles/show/Stefsunyanzi/timeline/tweets?include_available_features=1&include_entities=1&max_position=1074641543489716225&reset_error_state=false   1165834551605653504
#这个地方可以用下面这个url获取到最开始的max_position，当前页面用的是max_position，然后响应包json里的min_position就是下一页的max_position，循环获取，直到没有min_position。
url="https://twitter.com/i/profiles/show/Stefsunyanzi/timeline/tweets?include_available_features=1&include_entities=1"
proxies={'http':'127.0.0.1:10809','https':'127.0.0.1:10809'}
tweets=requests.get(url,proxies=proxies)
tweets.encoding="utf-8"

with open("./text.txt",'a',encoding='utf-8') as f:
	text_json=json.loads(tweets.text)
	while(text_json["min_position"]):
		print(text_json["min_position"]+'\n')
		pre = re.compile('>(.*?)<')
		#items_html里面有些地方有回车符，导致正则不能提取帖子文本，一定要先去掉所有回车符
		text=text_json["items_html"].replace('\n','')
		#这个地方应该要用取得形式，从标签里面先取，然后再删除，版本一是直接删除所有标签这样做代码没有重用性而且去除很麻烦
		content=re.findall(r'data-aria-label-part="0">(.*?)</p>',text)
		for line in content:
			#把多余标签，pic.twitter.com和url去掉
			pattern = re.compile(r'<[^>]+>|pic.twitter.com/.*|http(.*?)&nbsp;|',re.S)
			line = re.sub(pattern ,'',line)
			line = re.sub('&#39;' ,'\'',line)
			line = re.sub('&lt;','<',line)
			line = re.sub('&gt;','>',line)
			line = re.sub('&amp;','&',line)
			line = re.sub('&quot;','"',line)
			line = re.sub(r'^@(.*?) @(.*?) |^@(.*?) ','',line)
			if(len(line)):
				#continue
				f.write(line+'\n')
		tweets=requests.get(url+'&max_position='+text_json["min_position"]+'&reset_error_state=false',proxies=proxies)
		text_json=json.loads(tweets.text)
		
