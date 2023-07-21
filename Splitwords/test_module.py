import codecs
from difflib import SequenceMatcher

def  ReadFile(filePath,encoding='utf-8'):
    with codecs.open(filePath,'r',encoding) as f:
        return f.read()

def WriteFile(filePath,content,encoding='gbk'):
    with codecs.open(filePath,'w',encoding) as f:
        f.write(content)

def UTF8_to_GBK(src,dst):
    content = ReadFile(src,encoding='utf-8')
    WriteFile(dst,content,encoding='gbk')
#可能会用到的转换编码的函数

def similarity(str1,str2):
    return SequenceMatcher(None,str1,str2).ratio()
#相似字符串匹配度函数

def build_dic(segments:list):
    key = []
    val = []
    for split_words in segments:
        key.append(split_words[0])
        val.append(split_words[1])
    dic = dict(zip(key,val))
    return dic

def rebuild_dic(dict1:dict,dict2:dict):
    for key in dict1:
        if key in dict1 and key in dict2:
            dict2[key] = dict1[key]
    re_dic = dict2
    return re_dic

def kwd_pic2map(keywords_attribute:dict):
    input_pic_type = []
    output_pic_type = {}
    pic_map = {'点状图': 'point','点图':'point','散点图':'point','柱状图': 'bar','柱形图':'bar',
                '柱型图':'bar','柱图':'bar','条形图':'bar','条型图':'bar','直方图':'bar','条图':'bar',
                '折线图': 'line','线图':'line','趋势':'line','走势':'line','区域图': 'area','刻度图': 'tick','矩形图': 'rect',
                '饼图':'pie', '饼状图':'pie','圆图':'pie','圆饼图':'pie','圆形图':'pie','圆型图':'pie'}
    keywords_list = list(keywords_attribute.keys())

    for i in range(0, len(keywords_list), 1):
        if keywords_attribute[keywords_list[i]] == 'nz':
            input_pic_type.append(keywords_list[i])

    for s1 in input_pic_type:
        for s2 in list(pic_map.keys()):
            if similarity(s1, s2) >= 0.55:
                output_pic_type[s1] = pic_map[s1]
                break
            else:
                continue
    return output_pic_type
#手动匹配图标类型关键字

def kwd_verb2map(keywords_attribute:dict):
    input_verb_type = []
    output_verb_type = {}
    verb_map = {'增长':'line','减少':'line','上升':'line','下降':'line'}
    keywords_list = list(keywords_attribute.keys())

    for i in range(0, len(keywords_list), 1):
        if keywords_attribute[keywords_list[i]] == 'v':
            input_verb_type.append(keywords_list[i])

    for s1 in input_verb_type:
        for s2 in list(verb_map.keys()):
            if similarity(s1, s2) >= 0.55:
                output_verb_type[s1] = verb_map[s1]
                break
            else:
                continue
    return output_verb_type
#手动匹配趋势动词关键字

def kwd_ad2map(allwords_attribute:dict):
    input_ad_type = []
    output_ad_type = {}
    ad_map = {'快':'line','慢':'line','好':'line','坏':'line','差':'line','高':'line','低':'line'}
    allwords_list = list(allwords_attribute.keys())

    for i in range(0, len(allwords_list), 1):
        if allwords_attribute[allwords_list[i]] == 'a':
            input_ad_type.append(allwords_list[i])
    for s1 in input_ad_type:
        for s2 in ad_map:
            if similarity(s1, s2) >= 0.55:
                output_ad_type[s1] = ad_map[s1]
                break
            else:
                continue
    return output_ad_type
#手动匹配程度形容词/副词关键字

def kwd_encoding2map(allwords_attribute:dict):
    output_encoding_type = {}
    encoding_map = {'颜色': 'color','渐变色':'color','形状': 'shape','型状':'shape','大小': 'size'}
    allwords_list = list(allwords_attribute.keys())

    for words in allwords_list:
        if words == '颜色' or words == '渐变色' or words == '形状' or words == '型状' or words == '大小':
            output_encoding_type[words] = encoding_map[words]

    return output_encoding_type

# def get_xyfield(input_xy,keywords_attribute,xy_field):
#     output_xy = {}
#     keywords_list = list(keywords_attribute.keys())
#     for i in range(0, len(keywords_list), 1):
#         if keywords_attribute[keywords_list[i]] == 'n':
#             input_xy.append(keywords_list[i])
#     # print(input_xy)
#     for s1 in input_xy:
#         for s2 in list(xy_field.keys()):
#             if similarity(s1, s2) >= 0.75:
#                 output_xy[s2] = xy_field[s2]
#                 break
#             else:
#                 continue
#     return output_xy
# #手动匹配xy轴关键字
#
# def get_xyfieldname(input_xy,keywords_attribute):
#     keywords_list = list(keywords_attribute.items())
#     for x in keywords_list:
#         if x[1] == 'n':
#             input_xy.append(x[0])
#     output_xy = []
#     for i in range(0,len(input_xy),1):
#         if input_xy[i] == '横坐标' or input_xy[i] == '纵坐标'or input_xy[i] == '竖坐标':
#             output_xy.append(input_xy[i+1])
#     return output_xy
# #手动匹配xy轴名称关键字
# def get_colors(keywords_attribute,std_colors):
#     output_colors = []
#     keywords_list = list(keywords_attribute.keys())
#     for x in keywords_list:
#         if x in std_colors:
#             output_colors.append(x)
#     return output_colors
# #手动匹配颜色关键字