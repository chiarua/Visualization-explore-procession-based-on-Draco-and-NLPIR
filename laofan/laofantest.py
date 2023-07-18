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
#引入draco和渲染器
d = drc.Draco()
renderer = AltairRenderer()
#载入数据
df: pd.DataFrame = vega_data.seattle_weather()
df.head()
#基础事实集的创建
data_schema = drc.schema_from_dataframe(df)
data_schema_facts = drc.dict_to_facts(data_schema)
input_spec_base = data_schema_facts + [
    "entity(view,root,v0).",
    "entity(mark,v0,m0)."
]
#推荐图表生成函数
def recommend_charts(
    spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i+1}",k:int =1
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
            #print('nihao'*10)
            chart = chart.configure_view(continuousWidth=130, continuousHeight=130)
        display(chart)
        chart.save('chart'+str(k)+'.html')

    return chart_specs
input_spec=input_spec_base
#添加约束条件
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
    k=0
    for cfg, spec in input_specs:
        k+=1
        labeler = lambda i: f"CHART {i + 1} ({' | '.join(cfg)})"
        recs = recs | recommend_charts(spec=spec, draco=draco, num=num, labeler=labeler,k=k)

    return recs
#用户输入约束条件
recommendations = rec_from_generated_spec(
    marks=["point", "bar"],
    fields=["weather", "temp_min", "date"],
    encoding_channels=["color", "shape", "size"],
    draco=d,
)
