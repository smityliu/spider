import requests
import re
import sys

url="https://weibo.com/"+sys.argv[1]+"?is_hot=1"
proxies={'http':'127.0.0.1:10809',
		'https':'127.0.0.1:10809'}
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
		'Cookie': 'SINAGLOBAL=6342952051978.048.1563851633682; _ga=GA1.2.1085309167.1567189019; _td=3acfee1f-afe9-4dd5-99cd-7f27ef188897; __gads=ID=58fca272a89fc17c:T=1567189021:S=ALNI_Ma-5xAmXDwxAgCP0a6ZAMxnasBUHw; UM_distinctid=16ce3beb7878cc-067d85ac6aa236-a7f1a3e-e1000-16ce3beb78886b; ALF=1605056402; SCF=Aru1DpoX6JGJMfCjHoixexaIIyRcAqEPdiNZaKZNE2U3tBC3fXiwErmxSwHHFRs4Y0v4YCfM9U27FH5UYkURGNo.; SUHB=0nlvlQLGAurZLQ; SUB=_2AkMqgIBhf8NxqwJRmP4TzmziaIxyww3EieKc3HG6JRMxHRl-yT9kqkgptRB6AQCujk1WPOogYBdk9iC_xcAVxEXzSXrh; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhxwVZb3JuuIB_qjqk.F2Zs; _s_tentry=www.baidu.com; UOR=,,www.baidu.com; Apache=7935616526844.526.1576224190270; ULV=1576224190284:69:3:2:7935616526844.526.1576224190270:1575891939279; TC-V5-G0=62b98c0fc3e291bc0c7511933c1b13ad; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; WBtopGlobal_register_version=307744aa77dd5677; login_sid_t=5257eab1c9c9eaddfe26e4e35ac5a5f4; cross_origin_proto=SSL; wb_view_log=1280*7201.5; TC-Page-G0=2f200ef68557e15c78db077758a88e1f|1576251407|1576251407'}
text= requests.get(url,headers=header)
text.encoding='utf-8'
with open('./weibo.txt','w',encoding='utf-8') as f:
	pattern=re.compile(r'\\n|\\t|\\r|\\')
	text=re.sub(pattern,'',text.text)
	info_1 = re.findall(r'<p class="info"><span>(.*?)</span></p>',text)
	info_2 = re.findall(r'<span class="item_text W_fl">(.*?)</span></li>',text)
	infos = info_1 + info_2
	for info in infos:
		info = re.sub(r'<.*?>','',info)
		print(info.replace(' ',''))