import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
#import img_processing_oprs as ipo

@st.cache_data
def load_data(input_file):
    df=pd.read_csv(input_file)
    return df

st.title("可视化推荐")
st.divider()

with st.sidebar:
    input_NL = st.text_input('您的需求', placeholder='add your requirements here')
    submit_button1 = st.button('提交',key='button1')

    if input_NL == '' and submit_button1:
        st.warning('make sure you have put your requirements in the box.')
        st.stop()

    if input_NL == '':
        st.stop()

    input_file = st.file_uploader('文件上传',type=['csv'])
    if input_file is None:
        st.stop()

    num = st.slider('生成数量', 0, 20, 5)
    if st.checkbox('显示数据'):
        st.subheader('数据')
        df = load_data(input_file)
        st.write(df)

    submit_button2 = st.button('开始生成', key='button2')

if submit_button2:
    with st.spinner('Wait for it...'):
        time.sleep(3)

    flag = 0
    for i in range(11, 17, 1):
        flag += 1
        if flag > num:
            break

        with open(f'.\\rec_ch{i}.html', "r") as f:
            h = f.read()
            components.html(h,height=400)


