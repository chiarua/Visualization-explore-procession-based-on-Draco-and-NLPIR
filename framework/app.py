import time
import pandas as pd
import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components

import img_processing_oprs as ipo

@st.cache_data
def load_data(input_file):
    df=pd.read_csv(input_file)
    return df

# modal1 = Modal(title="", key="modal_key", max_width=2000)

# if "confirm" not in st.session_state:
#     st.session_state["confirm"] = False

# def del_btn_click():
#     st.session_state["confirm"] = True


st.title("可视化推荐")
st.divider()

with st.sidebar:
    # output_address = st.text_input('输出地址',placeholder='add your output address here')
    # submit_button1 = st.button('确定',key='button1')

    input_NL = st.text_input('您的需求',placeholder='add your requirements here')
    submit_button2 = st.button('提交', key='button2')

    input_file = st.file_uploader('文件上传',type=['csv'])

    if input_file is None:
        st.stop()
    else:
        num = st.slider('生成数量', 0, 20, 5)
        if st.checkbox('显示数据'):
            st.subheader('数据')
            df = load_data(input_file)
            st.write(df)

ipo.f(input_NL,input_file,num)

with open("html\h.html","r") as f:
    h=f.read()
    components.html(h,height=600)

# submit_button3 = st.button('开始生成',key='button3')
# if submit_button3:
#     with modal1.container():
#         progress_bar = st.progress(0)
#         progress = 0
#         latest_iteration = st.empty()
#         for i in range(100):
#             time.sleep(0.02)
#             progress += 1
#             progress_bar.progress(progress)
#             txt1 = latest_iteration.text(f'processing {i + 1}%')
#         txt1.empty()
#         txt1.write('success')
#         time.sleep(1.5)
#         modal1.close()


