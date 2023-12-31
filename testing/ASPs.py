import warnings
import draco as drc
import pandas as pd
from draco.renderer import AltairRenderer

warnings.filterwarnings("ignore")


# Display utilities


# 绘制径向图
def radial_spec(field_name, value):
    n = field_name
    c = value
    spec = ['attribute(number_rows,root,1461).',
            f'entity(field,root,{c}).',
            f'attribute((field,name),{c},{c}).',
            f'attribute((field,type),{c},number).',
            f'entity(field,root,{n}).',
            f'attribute((field,name),{n},{n}).',
            f'attribute((field,type),{n},string).',
            'entity(view,root,0).',
            'attribute((view,coordinates),0,polar).',
            'entity(mark,0,1).',
            'attribute((mark,type),1,bar).',
            'entity(encoding,1,2).',
            'attribute((encoding,channel),2,x).',
            f'attribute((encoding,field),2,{n}).',
            'entity(encoding,1,3).',
            'attribute((encoding,channel),3,y).',
            f'attribute((encoding,field),3,{c}).',
            'attribute((encoding,aggregate),3,mean).',
            'entity(scale,0,4).',
            'attribute((scale,channel),4,x).',
            'attribute((scale,type),4,ordinal).',
            'entity(scale,0,5).',
            'attribute((scale,channel),5,y).',
            'attribute((scale,type),5,linear).',
            'attribute((scale,zero),5,true).']
    return spec


# 绘制饼图
def pie_spec(field_name):
    n = field_name
    spec = ['attribute(number_rows,root,1461).',
            f'entity(field,root,{n}).',
            f'attribute((field,name),{n},{n}).',
            f'attribute((field,type),{n},string).',
            'entity(view,root,0).',
            'attribute((view,coordinates),0,polar).',
            'entity(scale,0,sc).',
            'attribute((scale,channel),sc,color).',
            'attribute((scale,type),sc,categorical).'  # 颜色变化的形式是明确变化
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


# 绘制xy轴条形图
def xy_bar_spec(x, y):
    spec = ['attribute(number_rows,root,1461).',
            f'entity(field,root,{y}).',
            f'attribute((field,name),{y},{y}).',
            f'attribute((field,type),{y},number).',
            f'entity(field,root,{x}).',
            f'attribute((field,name),{x},{x}).',
            f'attribute((field,type),{x},string).',
            'entity(view,root,0).',
            'attribute((view,coordinates),0,cartesian).',

            'entity(scale,v0,sc).',
            'attribute((scale,channel),sc,color).',
            'attribute((scale,type),sc,categorical).'  # 颜色变化的形式是明确变化

            'entity(mark,0,1).',
            'attribute((mark,type),1,bar).',

            'entity(encoding,1,ec).',
            f'attribute((encoding,field),ec,{x}).',
            'attribute((encoding,channel),ec,color).',  # x轴按颜色变化

            'entity(encoding,1,2).',
            'attribute((encoding,channel),2,x).',
            f'attribute((encoding,field),2,{x}).',
            'entity(encoding,1,3).',
            'attribute((encoding,channel),3,y).',
            f'attribute((encoding,field),3,{y}).',
            'attribute((encoding,aggregate),3,mean).',
            'entity(scale,0,4).',
            'attribute((scale,channel),4,x).',
            'attribute((scale,type),4,ordinal).',
            'entity(scale,0,5).',
            'attribute((scale,channel),5,y).',
            'attribute((scale,type),5,linear).',
            'attribute((scale,zero),5,true).']
    return spec


# 折线加条形
def bar_line_spec(x, y, y2):
    spec = ['attribute(number_rows,root,1461).',

            f'entity(field,root,{y2}).',
            f'attribute((field,name),{y2},{y2}).',
            f'attribute((field,type),{y2},number).',

            f'entity(field,root,{y}).',
            f'attribute((field,name),{y},{y}).',
            f'attribute((field,type),{y},number).',

            f'entity(field,root,{x}).',
            f'attribute((field,name),{x},{x}).',
            f'attribute((field,type),{x},string).',

            'entity(view,root,v0).',
            'attribute((view,coordinates),v0,cartesian).',

            'entity(scale,v0,sc).',
            'attribute((scale,channel),sc,color).',
            'attribute((scale,type),sc,categorical).'  # 颜色变化的形式是明确变化

            'entity(mark,v0,m1).',
            'attribute((mark,type),m1,bar).',

            'entity(encoding,m1,e0).',
            'attribute((encoding,channel),e0,x).',
            f'attribute((encoding,field),e0,{x}).',

            'entity(encoding,m1,e1).',
            'attribute((encoding,channel),e1,y).',
            f'attribute((encoding,field),e1,{y}).',
            'attribute((encoding,aggregate),e1,mean).',

            'entity(scale,v0,s0).',
            'attribute((scale,channel),s0,x).',
            'attribute((scale,type),s0,ordinal).',
            'entity(scale,v0,s1).',
            'attribute((scale,channel),s1,y).',
            'attribute((scale,type),s1,linear).',
            'attribute((scale,zero),s1,true).',

            'entity(mark,v0,m2).',
            'attribute((mark,type),m2,line).',

            'entity(encoding,m2,m2e0).',
            'attribute((encoding,channel),m2e0,x).',
            f'attribute((encoding,field),m2e0,{x}).',

            'entity(encoding,m2,m2e1).',
            'attribute((encoding,channel),m2e1,y).',
            f'attribute((encoding,field),m2e1,{y2}).',
            'attribute((encoding,aggregate),m2e1,mean).',

            'entity(mark,v0,m3).',
            'attribute((mark,type),m3,point).',

            'entity(encoding,m3,m3e0).',
            'attribute((encoding,channel),m3e0,x).',
            f'attribute((encoding,field),m3e0,{x}).',

            'entity(encoding,m3,m3ec).',
            f'attribute((encoding,field),m3ec,{x}).',
            'attribute((encoding,channel),m3ec,color).',  # x轴按颜色变化

            'entity(encoding,m3,m3e1).',
            'attribute((encoding,channel),m3e1,y).',
            f'attribute((encoding,field),m3e1,{y2}).',
            'attribute((encoding,aggregate),m3e1,mean).', ]
    return spec


def percentage_spec(type1, type2):
    spec = [
        'attribute(number_rows,root,1461).',
        f'entity(field,root,{type1}).',
        f'attribute((field,name),{type1},{type1}).',
        f'attribute((field,type),{type1},number).',
        f'entity(field,root,{type2}).',
        f'attribute((field,name),{type2},{type2}).',
        f'attribute((field,type),{type2},string).',
        'entity(view,root,0).',
        'entity(mark,0,1).',
        'attribute((mark,type),1,bar).',
        'entity(encoding,1,2).',
        'attribute((encoding,channel),2,x).',
        'attribute((encoding,aggregate),2,count).',
        'attribute((encoding,stack),2,normalize).',
        'entity(encoding,1,3).',
        'attribute((encoding,channel),3,y).',
        f'attribute((encoding,field),3,{type1}).',
        'attribute((encoding,binning),3,10).',
        'entity(encoding,1,4).',
        'attribute((encoding,channel),4,color).',
        f'attribute((encoding,field),4,{type2}).',
        'entity(scale,0,5).',
        'attribute((scale,channel),5,x).',
        'attribute((scale,type),5,linear).',
        'attribute((scale,zero),5,true).',
        'entity(scale,0,6).',
        'attribute((scale,channel),6,y).',
        'attribute((scale,type),6,linear).',
        'entity(scale,0,7).',
        'attribute((scale,channel),7,color).',
        'attribute((scale,type),7,categorical).']
    return spec


def generate_by_spec(spec, charts, df, mark: str, field: str):
    d = drc.Draco()
    renderer = AltairRenderer()
    for model in d.complete_spec(spec, 1):
        spec = drc.answer_set_to_dict(model.answer_set)
        chart = renderer.render(spec=spec, data=df)
        charts.append([chart, model.cost[0], mark, ','.join([mark, field])])
        return model.cost[0]


def extra_recommend(new_fields, charts, df):
    A_fields, B_fields = [], []
    for i in range(len(new_fields)):
        if df[new_fields[i]].nunique() <= 10 and df[new_fields[i]].nunique() * 5 < len(df[new_fields]):
            A_fields.append(new_fields[i])
        else:
            B_fields.append(new_fields[i])
    for field in A_fields:
        generate_by_spec(pie_spec(field), charts, df, 'pie', field)
        for value in B_fields:
            generate_by_spec(percentage_spec(value, field), charts, df, 'percentage', field)
            if df[field].nunique() >= 5:
                generate_by_spec(radial_spec(field, value), charts, df, 'radial', field)


def get_extra_charts(charts: list, field: list, df: pd.DataFrame):
    extra_recommend(field, charts, df)
    return charts