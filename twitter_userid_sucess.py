import requests
import re
import sys
#查询用户名id
url='https://twitter.com/search?f=users&vertical=default&q='+sys.argv[1]+'&src=unkn'
proxies={'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
search = requests.get(url,proxies=proxies)

search.encoding = 'utf-8'
print('查询成功')
text=search.text
print(re.findall(r'data-name="(.*?) data-protected="false"',text))
print('\n')
print(re.findall(r'<span class="username u-dir" dir="ltr">@<b class="u-linkComplex-target">(.*?)</b></span>',text))