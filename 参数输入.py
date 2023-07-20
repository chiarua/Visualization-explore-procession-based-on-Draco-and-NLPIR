def get_users_restriction(df):
    keywords=dict()
    #有用的关键词
    keyword_map = {'颜色': 'color','渐变色':'color','形状': 'shape','型状':'shape','大小': 'size','点状图': 'point','点图':'point',
                   '散点图':'point','柱状图': 'bar','柱形图':'bar','柱型图':'bar','柱图':'bar','条形图':'bar','条型图':'bar','直方图':'bar',
                   '条图':'bar','折线图': 'line','线图':'line','趋势':'line','走势':'line','区域图': 'area','刻度图': 'tick','矩形图': 'rect',
                   '饼图':'pie','饼状图':'pie','圆图':'pie','圆饼图':'pie','圆形图':'pie','圆型图':'pie','增长':'line','减少':'line',
                   '上升':'line','下降':'line','快':'line','慢':'line','好':'line','坏':'line','差':'line','高':'line','低':'line'}

    #参数分类
    mark_type=['bar','point','line','area','tick','rect','pie']
    encoding_channel_type=['color','shape','size']

    #生成总参数列表后分类
    lst = [keywords[key] for key in keywords if key in keyword_map]
    new_marks=[i for i in lst if i in mark_type]
    new_encoding_channels=[i for i in lst if i in  encoding_channel_type]
    new_fields = input('fields:').split()

    #判断是否是饼图
    polar = 'pie' in new_marks
    if polar:
        new_marks = []
    #设置默认参数
    if not new_marks:
        new_marks = ['point', 'bar', 'line', 'area', 'tick', 'rect'] if not polar else ['bar']

    x_and_y = len(new_fields) == 3 and new_fields[1] == 'and'
    if x_and_y:
        new_fields.remove('and')
    if not new_fields:
        new_fields = df.columns.tolist()

    #设置默认参数
    if not new_encoding_channels:
        new_encoding_channels = ['color', 'shape', 'size', 'x', 'y'] if not polar else ['x']
    #仅有x,y轴情况
    if x_and_y:
        new_encoding_channels = ['x', 'y']

    #去重
    new_marks=list(set(new_marks))
    new_encoding_channels=list(set(new_encoding_channels))

    return [new_marks, new_fields, new_encoding_channels, polar]