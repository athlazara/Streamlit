import streamlit as st
from PIL import Image
from opentrons import robot, containers, instruments
from opentrons.util import environment

switch = False
ports = ['COM1']#robot.get_serial_ports_list()
ports += ['断开连接']
red = Image.open('red circle.jpg')
green = Image.open('green circle.jpg')

# 界面
st.title('连接测试')

col1, col2, col3 = st.columns(3)
with col1:
    port = st.selectbox('请选择端口：', ports)
    if port!='断开连接':
        try:
            #robot.connect(port)
            switch = True
        except (FileNotFoundError, WindowsError):
            pass
    else:
        if switch == True:
            robot.disconnect()
            switch = False
with col2:
    st.header('连接状态：')
with col3:
    if not switch:
        st.image(red, width=70)
    else:
        st.image(green, width=70)

environment.refresh()
path = environment.get_path('CALIBRATIONS_FILE')
st.write('定位文件路径：')
st.code(path)

col1, col2 = st.columns(2)
with col1:
    if switch:
        if st.button('复位', disabled=False):
            robot.home()
            st.write('已复位')
    else:
        st.button('复位', disabled=True)
with col2:
    with open('calibrations.json', "r") as file:
        st.download_button(
            label="下载定位文件",
            data=file,
            file_name="calibrations.json",
            mime="json")
