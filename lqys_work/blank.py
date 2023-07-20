import sys
import pynlpir
import importlib
from Splitwords import test_module as split

importlib.reload(sys)

pynlpir.open()

s = '我想要一个能够比较不同城市空气质量的图表，这个图表应该直观生动，' \
    '能够清楚地展示出哪些城市的空气质量好，哪些城市的空气质量差。'

pynlpir.nlpir.ImportUserDict('userdic.txt'.encode('utf-8'))

segments1 = pynlpir.segment(s.encode('utf-8'),pos_tagging=True,pos_english=True,pos_names=None)
segments2 = pynlpir.get_key_words(s.encode('utf-8'),weighted=True)

dict1 = split.build_dic(segments1)
dict2 = split.build_dic(segments2)
dict3 = split.rebuild_dic(dict1,dict2)


print(split.kwd_pic2map(dict3))
print(split.kwd_verb2map(dict3))
print(split.kwd_ad2map(dict1))
print(split.kwd_encoding2map(dict1))
