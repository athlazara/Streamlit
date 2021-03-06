import streamlit as st
import pandas as pd
from bokeh.plotting import figure

#用empty会每次打印内容后再擦除，刷帧时能看到，视觉效果差
#head = st.empty()
#with head.container():
#    st.title('测速模型')
#    st.subheader('速度、加速度与距离公式：')
#    st.latex(r'\boxed{S = \frac12 a{t_1}^2 + V_{max} t_2}')# \times 

#@st.cache
def reset_x():
    st.session_state.a_0 = 1550
    st.session_state.m_0 = 30000
    st.session_state.d_0 = 419.35

#@st.cache 使用后停留在当前值，不再刷新变量
def reset_y():
    st.session_state.a_0 = 1550
    st.session_state.m_0 = 20000
    st.session_state.d_0 = 297.49

with st.sidebar.expander("设定参数"):
    a = st.slider('选择加速度', 0, 2000, 1550, key='a_0')
    st.write("*当前加速度为*：", a, "mm/s²")
    
    m = st.slider('设定速度上限', 0, 40000, 30000, key='m_0')
    st.write("*当前加速度为*：", m, "mm/min")
    v_max = m/60

    d = st.number_input('设定距离基线', value=419.35, min_value=0.00, key='d_0')
    st.write("*对标最终距离为*：", float('%.2f'%d), "mm")
    base_line = [d for i in range(20)]

    col1, col2 = st.columns(2)
    with col1:
        reset_X = st.button('X轴默认值', on_click=reset_x) #streamlit会自动删除按键名内空格,'\n'回车也没有效果
    with col2:
        reset_Y = st.button('Y轴默认值', on_click=reset_y)

button_1 = st.sidebar.checkbox('时间、速度与距离表')
button_2 = st.sidebar.checkbox('综合显示图')

data = []
time = []
speed = []
distance = []
for i in range(20):
    unit = []
    t = (i+1)/20
    v = a*t
    if v>=v_max:
        v = v_max
        t1 = v_max/a
        s1 = 1/2*a*t1*t1
        t2 = t-t1
        s2 = v_max*t2
        s = s1+s2
    else:
        s = 1/2*a*t*t
    time.append(t)
    speed.append(v)
    distance.append(s)
    unit = ['%.1f'%t, '%.0f'%v, '%.2f'%s]
    data.append(unit)
final_distance = s

if button_1 and not button_2:
    #head.empty()
    st.subheader('时间、速度与距离表：')
    df = pd.DataFrame(data, columns=('时间(s)', '速度(mm/s)', '距离(mm)'))
    #print(df.round({'时间(s)':2, '速度(mm/s)':2, '距离(mm)':2})) 无效,streamlit会自动填充小数位数
    st.dataframe(df.style.set_properties(**{'text-align': 'right'}), 300, 620)

elif not button_1 and button_2:
    #head.empty()
    st.subheader('综合显示图：')
    p = figure(title='速度&距离', x_axis_label='时间(s)', y_axis_label='mm/s & mm')
    p.line(time, base_line, legend_label='基线', line_width=2, color="green")
    p.vbar(x=time, top=distance, legend_label="距离", width=0.025, bottom=0, color="red")
    p.line(time, speed, legend_label='速度', line_width=2, color="blue")
    p.frame_width = 600
    p.height = 600
    p.legend.location = "top_left"
    st.bokeh_chart(p, use_container_width=True)

elif button_1 and button_2:
    #head.empty()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('时间、速度与距离表：')
        df = pd.DataFrame(data, columns=('时间(s)', '速度(mm/s)', '距离(mm)'))
        st.dataframe(df.style.set_properties(**{'text-align': 'right'}), 300, 310)
    
    with col2:
        st.subheader('综合显示图：')
        p = figure(title='速度&距离', x_axis_label='时间(s)', y_axis_label='mm/s & mm')
        p.line(time, base_line, line_width=2, color="green") #, legend_label='基线'
        p.vbar(x=time, top=distance, width=0.025, bottom=0, color="red") #, legend_label="距离"
        p.line(time, speed, line_width=2, color="blue") #, legend_label='速度'
        p.frame_width = 340 #width无效,frame_width会自动填充宽度
        p.height = 340
        st.bokeh_chart(p, use_container_width=True)

else:
    with st.container():
        st.title('测速模型')
        st.subheader('速度、加速度与距离公式：')
        st.latex(r'\boxed{S = \frac12 a{t_1}^2 + V_{max} t_2}')# \times 
