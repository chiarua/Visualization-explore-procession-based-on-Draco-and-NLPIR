from IPython.display import display, Markdown
import draco as drc
import pandas as pd
import altair as alt
from draco.renderer import AltairRenderer
import warnings
import os
from collections import defaultdict
from testing import ASPs

warnings.filterwarnings("ignore")


# Suppressing warnings raised by altair in the background
# (iteration-related deprecation warnings)




class ImgOpr:
    def __init__(self):
        self.path=''
        self.output_path=''
        self.df=self.get_csvfile()
        self.charts=[]
        self.d=drc.Draco()
        self.renderer = AltairRenderer()
        self.input_spec_base = self.generate_spec_base()
        self.n_marks,self.n_fields,self.n_encoding_channels= self.get_users_restriction()

    def recommend_charts(
            self,cfg: list, spec: list[str], draco: drc.Draco, num: int = 5, labeler=lambda i: f"CHART {i + 1}"
    ) -> dict[str, dict]:
        # Dictionary to store the generated recommendations, keyed by chart name
        chart_specs = {}
        for i, model in enumerate(draco.complete_spec(spec, num)):
            chart_name = labeler(i)
            spec = drc.answer_set_to_dict(model.answer_set)
            chart_specs[chart_name] = drc.dict_to_facts(spec)

            print(chart_name)
            print(f"COST: {model.cost}")
            chart = self.renderer.render(spec=spec, data=df)
            # Adjust column-faceted chart size

            if (
                    isinstance(chart, alt.FacetChart)
                    and chart.facet.column is not alt.Undefined
            ):
                chart = chart.configure_view(continuousWidth=130, continuousHeight=130)
            display(chart)
            self.charts.append([chart, model.cost, cfg[0], ','.join(cfg)])

        return chart_specs

    def get_path(self):
        self.path=input("Please input the path of the csv file: ")

    def get_output_path(self):
        self.output_path=input("Please input the address where you want the picture to be output: ")

    def get_csvfile(self):
        df = pd.read_csv(self.path)
        return df

    def generate_spec_base(self):
        data_schema = drc.schema_from_dataframe(self.df)
        data_schema_facts = drc.dict_to_facts(data_schema)
        input_spec_base = data_schema_facts + [
            "entity(view,root,v0).",
            "entity(mark,v0,m0)."
        ]
        return input_spec_base

    def rec_from_generated_spec(
            self,
            marks: list[str],
            fields: list[str],
            encoding_channels: list[str],
            draco: drc.Draco,
            num: int = 1,
    ) -> dict[str, dict]:
        input_specs = [
            (
                (mark, field, enc_ch),
                self.input_spec_base
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
            recs = recs | self.recommend_charts(cfg=cfg, spec=spec, draco=draco, num=num, labeler=labeler)

        return recs

    def update_spec(self):
        recommendations = rec_from_generated_spec(
            marks=self.new_marks,
            fields=self.new_fields,
            encoding_channels=self.new_encoding_channels,
            draco=self.d,
        )

    def display_debug_data(self,draco: drc.Draco, specs: dict[str, dict]):
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
        chart.save(self.output_path + 'debugchart' + str(self.count_files_in_directory(output_path)) + '.html')

    def get_users_restriction(delf):
        s = input('输入你的需求:')

        # 有用的关键词
        keyword_map = {'颜色': 'color', '渐变色': 'color', '形状': 'shape', '型状': 'shape', '大小': 'size',
                       '点状图': 'point', '点图': 'point',
                       '散点图': 'point', '柱状图': 'bar', '柱形图': 'bar', '柱型图': 'bar', '柱图': 'bar',
                       '条形图': 'bar',
                       '条型图': 'bar', '直方图': 'bar',
                       '条图': 'bar', '折线图': 'line', '线图': 'line', '趋势': 'line', '走势': 'line',
                       '区域图': 'area',
                       '刻度图': 'tick', '矩形图': 'rect',
                       '饼图': 'pie', '饼状图': 'pie', '圆图': 'pie', '圆饼图': 'pie', '圆形图': 'pie', '圆型图': 'pie',
                       '增长': 'line', '减少': 'line',
                       '上升': 'line', '下降': 'line', '快': 'line', '慢': 'line', '好': 'line', '坏': 'line',
                       '差': 'line',
                       '高': 'line', '低': 'line'}

        # 参数分类
        mark_type = ['bar', 'point', 'line', 'area', 'tick', 'rect', 'pie']
        encoding_channel_type = ['color', 'shape', 'size']
        fields_type = self.df.columns.tolist()

        # 生成总参数列表后分类
        lst = [keyword_map[key] for key in keyword_map.keys() if key in s]
        new_marks = [i for i in lst if i in mark_type]
        new_encoding_channels = [i for i in lst if i in encoding_channel_type]
        new_fields = [i for i in fields_type if i in s]
        return [new_marks, new_fields, new_encoding_channels]

    def select_restriction(self):
        # 去重
        self.n_marks = list(set(self.n_marks))
        self.n_encoding_channels = list(set(self.n_encoding_channels))
        # 设置默认参数
        # 这样设置是不行的，需要对这里或者cost进行修改，不然出垃圾
        if not self.n_marks:
            self.n_marks = ['point', 'bar', 'line', 'area', 'tick', 'rect']

        if not self.n_fields:
            self.n_fields = self.df.columns.tolist()

        # 设置默认参数
        if not self.n_encoding_channels:
            self.n_encoding_channels = ['color', 'shape', 'size', 'x']

    def chart_save(self,n: int, c: list):
        mark_limit = 3
        mark = defaultdict(int)
        i = 0
        while i < n and c:
            if mark[c[0][2]] > mark_limit:
                c = c[1:]
                continue
            i += 1
            c[0][0].save(self.output_path + c[0][3] + '.html')
            mark[c[0][2]] += 1
            c = c[1:]

    def count_files_in_directory(self, directory_path):
        return len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name))])

test=ImgOpr()
test.get_path()
test.charts = sorted(charts, key=lambda x: x[1])
test.update_spec()
test.chart_save(100)


