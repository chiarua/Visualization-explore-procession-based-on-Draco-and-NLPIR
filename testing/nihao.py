import warnings

warnings.filterwarnings("ignore")
# Display utilities
from pprint import pprint
from IPython.display import display, Markdown
import draco as drc
import pandas as pd
from vega_datasets import data as vega_data
import altair as alt
from draco import dict_to_facts, answer_set_to_dict, run_clingo
from pprint import pprint

# Loading data to be explored
df: pd.DataFrame = vega_data.seattle_weather()
df=pd.read_csv("data\\cars_mod.csv")
df.head()
data_schema = drc.schema_from_dataframe(df)
#pprint(data_schema)
data_schema_facts = drc.dict_to_facts(data_schema)



#pprint(data_schema_facts)
from draco.renderer import AltairRenderer
d = drc.Draco()
renderer = AltairRenderer()
input_spec_base = data_schema_facts + [
    "entity(view,root,v0).",
    "entity(mark,v0,m0).",
]



input_spec = input_spec_base
#绘制饼图
def pie_spec(field_name):
 n=field_name
 spec=['attribute(number_rows,root,1461).',
 f'entity(field,root,{n}).',
 f'attribute((field,name),{n},{n}).',
 f'attribute((field,type),{n},string).',
 'entity(view,root,0).',
 'attribute((view,coordinates),0,polar).',
 'entity(mark,0,1).',
 'attribute((mark,type),1,bar).',
 'entity(encoding,1,2).',
 'attribute((encoding,channel),2,y).',
 'attribute((encoding,aggregate),2,count).',
 'attribute((encoding,stack),2,zero).',
 'entity(encoding,1,3).',
 'attribute((encoding,channel),3,color).',
 f'attribute((encoding,field),3,{n}).']
 return spec
def generate_by_spec(spec):
 for model in run_clingo(spec):
     answer_set = model.answer_set
     dic = drc.answer_set_to_dict(answer_set)
     chart=renderer.render(dic,df)
     chart.save('output_path')

generate_by_spec(pie_spec('field_name'))


