import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    
if __name__ == "__main__":
	#按表格形式读入数据
	#一定要记得在数据最前面加一个标题content，不然数据格式会出错
	df = pd.read_table("./text.txt", encoding='utf-8')
	#print(df)
	df["content_cutted"] = df.content.apply(chinese_word_cut)
	
	#设置停用词,设为None不使用停用词，设为None且max_df∈[0.7, 1.0)将自动根据当前的语料库建立停用词表
	stpwrdpath ="./stop_words.txt"
	with open(stpwrdpath, 'r',encoding='utf-8') as fp:
		stop_words = fp.read() # 提用词提取
	stop_words = stop_words.splitlines()
	
	#提取1000个关键词
	n_features = 1000
	tf_vectorizer = CountVectorizer(strip_accents = 'unicode', max_features=n_features,stop_words=stop_words,max_df=0.5,min_df=3)
	tf = tf_vectorizer.fit_transform(df.content_cutted)
	
	n_topics = 8
	lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,learning_method='online',learning_offset=50,random_state=0)
	lda.fit(tf)
	n_top_words = 5
	tf_feature_names = tf_vectorizer.get_feature_names()
	print_top_words(lda, tf_feature_names, n_top_words)
	
	#浏览器绘图
	data = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
	pyLDAvis.show(data)
	print("over")