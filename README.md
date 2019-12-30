# 新浪微博爬虫+推特爬虫(模拟登录+免登录，不使用api) spider for twitter
## 本项目实现的最初目的是为了从用户发的帖子中分析人物兴趣属性

使用前，请在脚本中修改本机代理端口，或者开全局模式后，把requests中的proxies去掉

使用模拟登录的时候，麻烦自己截取一下流量包填入字段，这里我把自己的信息都删除了，各位自己截取

## weibo_login.py（微博模拟登录）

使用的时候，现在代码里面写入你的用户名密码，还有在header里面补上你的cookie，这个很简单，只要看了weibo.cn，截取一下流量包就全都有了

使用方法：
python3 weibo_login.py

## twitter_login_test.py（推特模拟登录）
使用的时候，现在代码里面写入你的用户名密码，或者你不写也可以，不影响，在header里面补上你的authorization和cookie，x-scrftoken就是cookie里的ct0字段，截取一下流量包就全都有了

使用方法：
python3 twitter_login_test.py

## twitter_userid_sucess.py：
显示两列，一列是相关用户昵称，一列是对应用户昵称的用户id

使用方法：
python3 twitter_userid_sucess.py "你想要搜索的内容"

example python3 twitter_userid_sucess.py smity

## tweets_text_success.py
成功后会在同目录下生成一个text.txt文件，数据量太大可以提前用ctrl + c 结束脚本运行，一样会有数据

使用方法：
python3 tweets_text_success.py "用户id"

example python3 tweets_text_success.py smityliu

## lda.py
会自动训练出n_topics个主题，依照使用者需求规定主题数量和关键词数量，训练成功后弹出可视化的浏览器界面

使用方法：
python3 lda.py

example python3 lda.py

## weibo_indentity.py
使用方法：
python3 weibo_indentity.py "用户id"

example python3 weibo_indentity.py smityliu
