from IPython.display import display, Markdown
import draco as drc
import pandas as pd
from vega_datasets import data as vega_data
import altair as alt
from draco.renderer import AltairRenderer
import warnings
import os
from collections import defaultdict

warnings.filterwarnings("ignore")


# Suppressing warnings raised by altair in the background
# (iteration-related deprecation warnings)


def count_files_in_directory(directory_path):
    return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name))])


# 推荐函数
def recommend_charts(
        cfg:list, spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i + 1}"
) -> dict[str, dict]:
    # Dictionary to store the generated recommendations, keyed by chart name
    chart_specs = {}
    for i, model in enumerate(draco.complete_spec(spec, num)):
        chart_name = labeler(i)
        spec = drc.answer_set_to_dict(model.answer_set)
        chart_specs[chart_name] = drc.dict_to_facts(spec)

        print(chart_name)
        print(f"COST: {model.cost}")
        chart = renderer.render(spec=spec, data=df)
        # Adjust column-faceted chart size

        if (
                isinstance(chart, alt.FacetChart)
                and chart.facet.column is not alt.Undefined
        ):
            chart = chart.configure_view(continuousWidth=130, continuousHeight=130)
        display(chart)
        charts.append([chart, model.cost, cfg[0], ','.join(cfg)])

    return chart_specs


def get_csvfile(file_path):
    df = pd.read_csv(file_path)
    return df


def get_jsonfile(file_path):
    df = pd.read_json(file_path)
    return df


def get_output_address():
    address = input("Please input the address where you want the picture to be output: ")
    return address


# 基础事实集的创建
def generate_spec_base(df):
    data_schema = drc.schema_from_dataframe(df)
    data_schema_facts = drc.dict_to_facts(data_schema)
    input_spec_base = data_schema_facts + [
        "entity(view,root,v0).",
        "entity(mark,v0,m0)."
    ]
    return input_spec_base


# 从更新的事实集中直接生成图表
# 用到了recommend函数
def rec_from_generated_spec(
        marks: list[str],
        fields: list[str],
        encoding_channels: list[str],
        draco: drc.Draco,
        num: int = 1,
) -> dict[str, dict]:
    input_specs = [
        (
            (mark, field, enc_ch),
            input_spec_base
            + [
                f"attribute((mark,type),m0,{mark}).",
                "entity(encoding,m0,e0).",
                f"attribute((encoding,field),e0,{field}).",
                f"attribute((encoding,channel),e0,{enc_ch}).",
                # 暂时去掉
                # filter out designs with less than 3 encodings
                ":- {entity(encoding,_,_)} < 3.",
                # exclude multi-layer designs
                ":- {entity(mark,_,_)} != 1.",
            ],
        )
        for mark in marks
        for field in fields
        for enc_ch in encoding_channels
    ]
    recs = {}
    # k = 0
    for cfg, spec in input_specs:
        # k += 1
        labeler = lambda i: f"CHART {i + 1} ({' | '.join(cfg)})"
        recs = recs | recommend_charts(cfg=cfg, spec=spec, draco=draco, num=num, labeler=labeler)

    return recs


# 用户输入约束条件的推荐函数
def update_spec(new_marks, new_fields, new_encoding_channels):
    recommendations = rec_from_generated_spec(
        marks=new_marks,
        fields=new_fields,
        encoding_channels=new_encoding_channels,
        draco=d,
    )
    # display_debug_data(draco=d, specs=recommendations)


# Parameterized helper to avoid code duplication as we iterate on designs
# 用于查看规范违反情况的函数
def display_debug_data(draco: drc.Draco, specs: dict[str, dict]):
    debugger = drc.DracoDebug(specs=specs, draco=draco)
    chart_preferences = debugger.chart_preferences
    display(Markdown("**Raw debug data**"))
    display(chart_preferences.head())

    display(Markdown("**Number of violated preferences**"))
    num_violations = len(
        set(chart_preferences[chart_preferences["count"] != 0]["pref_name"])
    )
    num_all = len(set(chart_preferences["pref_name"]))
    display(
        Markdown(
            f"*{num_violations} preferences are violated out of a total of {num_all} preferences (soft constraints)*"
        )
    )

    display(
        Markdown(
            "Using `DracoDebugPlotter` to visualize the debug `DataFrame` produced by `DracoDebug`:"
        )
    )
    plotter = drc.DracoDebugPlotter(chart_preferences)
    plot_size = (600, 300)
    chart = plotter.create_chart(
        cfg=drc.DracoDebugChartConfig.SORT_BY_COUNT_SUM,
        violated_prefs_only=True,
        plot_size=plot_size,
    )
    chart.save(output_path + 'debugchart' + str(count_files_in_directory(output_path)) + '.html')


def get_users_restriction(df):
    s = input('输入你的需求:')

    # 有用的关键词
    keyword_map = {'颜色': 'color', '渐变色': 'color', '形状': 'shape', '型状': 'shape', '大小': 'size',
                   '点状图': 'point', '点图': 'point',
                   '散点图': 'point', '柱状图': 'bar', '柱形图': 'bar', '柱型图': 'bar', '柱图': 'bar', '条形图': 'bar',
                   '条型图': 'bar', '直方图': 'bar',
                   '条图': 'bar', '折线图': 'line', '线图': 'line', '趋势': 'line', '走势': 'line', '区域图': 'area',
                   '刻度图': 'tick', '矩形图': 'rect',
                   '饼图': 'pie', '饼状图': 'pie', '圆图': 'pie', '圆饼图': 'pie', '圆形图': 'pie', '圆型图': 'pie',
                   '增长': 'line', '减少': 'line',
                   '上升': 'line', '下降': 'line', '快': 'line', '慢': 'line', '好': 'line', '坏': 'line', '差': 'line',
                   '高': 'line', '低': 'line'}

    # 参数分类
    mark_type = ['bar', 'point', 'line', 'area', 'tick', 'rect', 'pie']
    encoding_channel_type = ['color', 'shape', 'size']
    fields_type = df.columns.tolist()

    # 生成总参数列表后分类
    lst = [keyword_map[key] for key in keyword_map.keys() if key in s]
    new_marks = [i for i in lst if i in mark_type]
    new_encoding_channels = [i for i in lst if i in encoding_channel_type]
    new_fields = [i for i in fields_type if i in s]
    return [new_marks, new_fields, new_encoding_channels]


def select_restriction(df):
    new_marks, new_fields, new_encoding_channels = get_users_restriction(df)
    # 去重
    new_marks = list(set(new_marks))
    new_encoding_channels = list(set(new_encoding_channels))
    # 设置默认参数
    # 这样设置是不行的，需要对这里或者cost进行修改，不然出垃圾
    if not new_marks:
        new_marks = ['point', 'bar', 'line', 'area', 'tick', 'rect']

    if not new_fields:
        new_fields = df.columns.tolist()

    # 设置默认参数
    if not new_encoding_channels:
        new_encoding_channels = ['color', 'shape', 'size', 'x']


    return [new_marks, new_fields, new_encoding_channels]


# 保存函数(按照cost)
def chart_save(n: int, c: list):
    mark_limit = 5
    mark = defaultdict(int)
    i = 0
    while i < n and c:
        if mark[c[0][2]] > mark_limit:
            c = c[1:]
            continue
        i += 1
        c[0][0].save(output_path + c[0][3] + '.html')
        mark[c[0][2]] += 1
        c = c[1:]


path = input("Please input the path of the csv file: ")
charts = []
output_path = get_output_address() + '\\'
df = get_csvfile(path)
d = drc.Draco()
renderer = AltairRenderer()
input_spec_base = generate_spec_base(df)
# recommendations = recommend_charts(spec=input_spec_base, draco=d, num=5)
# display_debug_data(draco=d, specs=recommendations)
n_marks, n_fields, n_encoding_channels = select_restriction(df)
charts = sorted(charts, key=lambda x: x[1])
update_spec(n_marks, n_fields, n_encoding_channels)
ASPs.get_extra_charts(charts, n_fields)
chart_save(100, charts)
# display_debug_data(draco=d, specs=recommendations)
# C:\Users\y9270\PycharmProjects\pythonProject2\data\driving.csv
# C:\Users\y9270\PycharmProjects\pythonProject2\Charts
# point line bar
# weather wind date
# 我想要一张反映weather和wind关系的图
