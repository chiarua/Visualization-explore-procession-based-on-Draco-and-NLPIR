# Suppressing warnings raised by altair in the background
# (iteration-related deprecation warnings)
import warnings
from draco.renderer import AltairRenderer

warnings.filterwarnings("ignore")
# Display utilities
from pprint import pprint
from IPython.display import display, Markdown
import draco as drc
import pandas as pd
from vega_datasets import data as vega_data
import altair as alt
#读入数据

# 从文件中读取数据
file_path = 'cars.csv'  # 替换为你的文件路径
dataframe = pd.read_csv(file_path)  # 假设文件是CSV格式，如果是其他格式请使用相应的读取函数



# 载入数据
df: pd.DataFrame = dataframe
#df: pd.DataFrame = vega_data.seattle_weather()
df.head()

#根据数据生成结构
data_schema = drc.schema_from_dataframe(df)
#pprint(data_schema)

#根据结构生成基础事实集(已有数据事实+view+mark)
data_schema_facts = drc.dict_to_facts(data_schema)
#pprint(data_schema_facts)

input_spec_base = data_schema_facts + [
    "entity(view,root,v0).",
    "entity(mark,v0,m0).",
]
#"attribute((mark,type),m0,bar)"
d = drc.Draco()
renderer = AltairRenderer()   #用于渲染图表

#定义生成推荐的函数
def recommend_charts(
    #事实集           draco             推荐数量       图表标签(图表1,图表2,...)
    spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i+1}"
) -> dict[str, dict]:
    # Dictionary to store the generated recommendations, keyed by chart name
    chart_specs = {}
    print('running')
    for i, model in enumerate(draco.complete_spec(spec, num)):#利用draco中的函数和传入事实集生成(推荐图表的事实集)的集合
        chart_name = labeler(i)#以标签为推荐图表命名
        #产生推荐事实集
        spec = drc.answer_set_to_dict(model.answer_set)
        chart_specs[chart_name] = drc.dict_to_facts(spec)

        #print(chart_name)
        #print(f"COST: {model.cost}")
        #利用推荐事实集生成图表
        chart = renderer.render(spec=spec, data=df)
        # 调整图表大小
        if (
            isinstance(chart, alt.FacetChart)
            and chart.facet.column is not alt.Undefined
        ):
            print('false')
            chart = chart.configure_view(continuousWidth=130, continuousHeight=130)
        #显示图表
        print(type(chart))
        filename='filename'+str(i)+'.html'
        chart.save(filename)
        #display(chart)
    #打印图表的事实集
    #print(chart_specs)
    return chart_specs
input_spec = input_spec_base
recommend_charts(spec=input_spec, draco=d);

