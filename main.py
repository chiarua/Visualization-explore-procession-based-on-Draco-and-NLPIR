# 以下是测试调用
from img_processing_oprs import *


path = input("Please input the path of the csv file: ")
output_path = get_output_address() + '\\'
df = get_csvfile(path)
d = drc.Draco()
renderer = AltairRenderer()
input_spec_base = generate_spec_base(df)
#recommendations = recommend_charts(spec=input_spec_base, draco=d, num=5)
#display_debug_data(draco=d, specs=recommendations)
# 其实看不懂debug的图表，但可以做测试
n_marks, n_fields, n_encoding_channels, polar= get_users_restriction(df)
print(n_marks,n_fields,n_encoding_channels,polar)
if polar:
    input_spec_base.append('attribute((view,coordinates),v0,polar).')
update_spec(n_marks, n_fields, n_encoding_channels)
#display_debug_data(draco=d, specs=recommendations)
# C:\Users\27217\Documents\GitHub\testing-7-16-23\laofan\data\weather.csv
# C:\Users\27217\Desktop\testing generate charts
# point line bar
# weather wind date