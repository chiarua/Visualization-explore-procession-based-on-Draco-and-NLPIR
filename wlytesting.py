from IPython.display import display, Markdown
import draco as drc
import pandas as pd
from vega_datasets import data as vega_data
import altair as alt
from draco.renderer import AltairRenderer
import warnings

warnings.filterwarnings("ignore")


# Suppressing warnings raised by altair in the background
# (iteration-related deprecation warnings)

# 原有推荐函数
def recommend_charts(
        spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i + 1}"
):
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
        print(output_path + 'filename' + str(i) + '.html')
        chart.save(output_path + 'filename' + str(i) + '.html')

    # return chart_specs(-> dict[str, dict])


def get_csvfile(file_path):
    df = pd.read_csv(file_path)
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


# 被generate_spec_base()函数代替
'''
df: pd.DataFrame = get_csvfile("")
df.head()

data_schema = drc.schema_from_dataframe(df)
data_schema_facts = drc.dict_to_facts(data_schema)
input_spec_base = data_schema_facts + [
    "entity(view,root,v0).",
    "entity(mark,v0,m0)."
]
'''

path = input("Please input the path of the csv file: ")
output_path = get_output_address() + '\\'
df = get_csvfile(path)
d = drc.Draco()
renderer = AltairRenderer()
input_spec_base = generate_spec_base(df)
recommend_charts(spec=input_spec_base, draco=d)
# pprint(input_spec_base)
# C:\Users\27217\Documents\GitHub\testing-7-16-23\laofan\cars.csv
# C:\Users\27217\Desktop\testing generate charts
