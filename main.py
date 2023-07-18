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
from draco.renderer import AltairRenderer

d = drc.Draco()
renderer = AltairRenderer()



#读入数据
def load_data(file_path):
    dataframe=pd.read_csv(file_path)
    return dataframe


def spec_base_generate(dataframe,mark_type='bar'):
    data_schema = drc.schema_from_dataframe(dataframe)
    data_schema_facts = drc.dict_to_facts(data_schema)
    spec_base = data_schema_facts + [
        "entity(view,root,v0).",
        "entity(mark,v0,m0)."
    ]
    return spec_base


def recommend_charts(
    spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i+1}"
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
            print('nihao')
            chart = chart.configure_view(continuousWidth=130, continuousHeight=130)
        display(chart)

    return chart_specs

dataframe=load_data('cars.csv')
dataframe.head()
#print(dataframe)

'''
df: pd.DataFrame = vega_data.seattle_weather()
df.head()
dataframe=df
#print(dataframe)
'''



spec_base=spec_base_generate(dataframe)
#print(spec_base)
recommend_charts(spec_base,d)



