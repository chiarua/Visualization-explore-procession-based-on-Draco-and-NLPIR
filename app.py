import time
import pandas as pd
import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components
from pathlib import Path

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


st.subheader("可视化推荐")
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
        num = st.slider('生成数量', 1, 20, 1)
        if st.checkbox('显示数据'):
            st.subheader('数据')
            df = load_data(input_file)
            st.write(df)

def delete_all_files_in_folder(folder_path):
    folder_path = Path(folder_path)

    for file_path in folder_path.glob("**/*"):
        if file_path.is_file():
            try:
                file_path.unlink()  # 删除文件
            except OSError as e:
                print(f"无法删除文件 '{file_path}'。错误信息：{e}")

def process_html_files(folder_path):

    folder_path = Path(folder_path)

    l=[]

    for file_path in folder_path.glob("**/*.html"):
        with open(file_path,"r") as f:
            h=f.read()
            l.append(h)
    return l

delete_all_files_in_folder(f"{Path.cwd()}/html/")
ipo.f(input_NL,input_file,num,f"{Path.cwd()}/html/")
html_list = process_html_files(f"{Path.cwd()}/html/")

# cols = st.columns(num)
# for i,col in enumerate(cols):
#     with col:
#         for i in process_html_files(f"{Path.cwd()}/html/"):
#             components.html(i,height=400,width=600)

tabs = st.tabs([str(i) for i in range(num)])
# for i,tab in enumerate(tabs):
#     with tab:
#         st.header("A cat")
for i,h in enumerate(html_list):
    st.write(i,len(html_list),len(tabs))
    with tabs[i]:
        components.html(h,height=400,width=600)
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


