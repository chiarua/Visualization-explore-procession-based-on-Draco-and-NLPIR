import os
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import class_img as img
import img_processing_oprs as ipo
from PIL import Image

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

    d={}
    for file_path in folder_path.glob("**/*.html"):
        n=file_path.stem
        with file_path.open("r") as f:
            h=f.read()
            d[n]=h
    return d

st.set_page_config(page_title='可视化图形推荐系统',
                   page_icon='https://img2.baidu.com/it/u=88880420,2'
                             '148161512&fm=253&fmt=auto&app=120&f=JPEG?w=189&h=190',
                   layout='wide',
                   initial_sidebar_state='collapsed',
                   menu_items={
                        'Get Help': 'https://github.com/chiarua/Visualization-explore-procession-based-on-Draco-and-NLPIR'
                   }
)
st.markdown('<span style="font-size: 40px;">**可视化推荐**</span>', unsafe_allow_html=True)
st.divider()

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

with st.sidebar:
    st.header('操作界面')

    st.markdown('**您的需求**')
    input_NL = st.text_input('',placeholder='add your requirements here',label_visibility='collapsed')

    if input_NL == '':
        st.warning('make sure you have put your requirements in the box.')
        st.stop()

    st.markdown('**文件上传**')
    input_file = st.file_uploader('',type=['csv'],label_visibility='collapsed')

    if input_file is None:
        st.stop()
    else:
        st.markdown('**生成模式**')
        box = st.radio('', options=['Ordinary', 'Accurate'], horizontal=True,label_visibility='collapsed')
        if box == 'Ordinary':
            st.markdown('**生成数量**')
            num = st.slider('', 1, 20, 3,label_visibility='collapsed')
            df = load_data(input_file)
            if st.checkbox('显示数据', key='check2'):
                st.subheader('数据')
                st.write(df)
            submit_button2 = st.button('开始生成', key='button2')
        elif box == 'Accurate':
            df = load_data(input_file)
            if st.checkbox('显示数据', key='check2'):
                st.subheader('数据')
                st.write(df)
            submit_button2 = st.button('开始生成', key='button2')

if submit_button2 and box == 'Ordinary':
    with st.spinner('Wait for it...'):
        os.makedirs('html', exist_ok=True)
        delete_all_files_in_folder(f"{Path.cwd()}/html/")
        ipo.f(input_NL,input_file,num,f"{Path.cwd()}/html/")
        html_dict = process_html_files(f"{Path.cwd()}/html/")
        time.sleep(0.5)
    tabs = st.tabs(["图"+str(i) for i in range(1,num+1)])
    for i,(hk,hv) in enumerate(html_dict.items()):
        with tabs[i]:
            components.html(hv,height=390)
            mark,field,channel=hk.split(",")
            with st.expander("details"):
                s=f"mark : {mark}\nfield : {field}\nchannel : {channel}"
                st.text(s)

elif submit_button2 and box == 'Accurate':
    with st.spinner('Wait for it...'):
        os.makedirs('html',exist_ok=True)
        delete_all_files_in_folder(f"{Path.cwd()}/html/")
        op = img.ImgOpr()
        op.opr_all(input_NL,input_file,3,f"{Path.cwd()}/html/")
        html_dict = process_html_files(f"{Path.cwd()}/html/")
        time.sleep(0.5)
    tabs = st.tabs(["图"+str(i) for i in range(1,3+1)])
    for i,(hk,hv) in enumerate(html_dict.items()):
        with tabs[i]:
            components.html(hv,height=390)
            mark,field,channel=hk.split(",")
            with st.expander("details"):
                s=f"mark : {mark}\nfield : {field}\nchannel : {channel}"
                st.text(s)
