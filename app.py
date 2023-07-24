import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

import img_processing_oprs as ipo

@st.cache_data
def load_data(input_file):
    df=pd.read_csv(input_file)
    return df

def delete_all_files_in_folder(folder_path):
    folder_path = Path(folder_path)

    for file_path in folder_path.glob("**/*"):
        if file_path.is_file():
            try:
                file_path.unlink()
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

st.subheader("可视化推荐")
st.divider()

with st.sidebar:
    input_NL = st.text_input('您的需求',placeholder='add your requirements here')
    if input_NL == '':
        st.warning('make sure you have put your requirements in the box.')
        st.stop()

    input_file = st.file_uploader('文件上传',type=['csv'])

    if input_file is None:
        st.stop()
    else:
        num = st.slider('生成数量', 1, 20, 1)
        df = load_data(input_file)
        if st.checkbox('显示数据'):
            st.subheader('数据')
            st.write(df)
    submit_button2 = st.button('开始生成', key='button2')

if submit_button2:
    with st.spinner('Wait for it...'):
        delete_all_files_in_folder(f"{Path.cwd()}/html/")
        ipo.f(input_NL,input_file,num,f"{Path.cwd()}/html/")
        html_list = process_html_files(f"{Path.cwd()}/html/")
    tabs = st.tabs([str(i) for i in range(num)])
    for i,h in enumerate(html_list):
        with tabs[i]:
            components.html(h,height=400)
            with st.expander("详细"):
                st.write("123")


