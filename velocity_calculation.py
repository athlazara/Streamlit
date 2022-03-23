import streamlit as st
import pandas as pd
from bokeh.plotting import figure

st.title('测速表')

st.subheader('速度、加速度与距离公式：')
st.latex(r'\boxed{S = \frac12 a{t_1}^2 + V_{max} t_2}')# \times 

a = st.slider('选择加速度', 0, 2000, 1550)
st.write("当前加速度为 ", a, "mm/s²")

m = st.slider('设定速度上限', 0, 30000, 30000)
st.write("当前加速度为 ", m, "mm/min")
v_max = m/60

st.subheader('时间、速度与距离表：')

data = []
time = []
speed = []
distance = []
base_line = []
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
    unit = ['%.2f'%t, '%.2f'%v, '%.2f'%s]
    data.append(unit)
    base_line.append(419.35)

df = pd.DataFrame(data, columns=('时间(s)', '速度(mm/s)', '距离(mm)'))
#print(df.round({'时间(s)':2, '速度(mm/s)':2, '距离(mm)':2})) 无效,streamlit会自动填充小数位数
st.dataframe(df.style.set_properties(**{'text-align': 'right'}), 300, 500)

st.subheader('散点图：')
p = figure(title='速度&距离', x_axis_label='时间(s)', y_axis_label='mm/s & mm')

p.line(time, base_line, legend_label='基线', line_width=2, color="green")
p.vbar(x=time, top=distance, legend_label="距离", width=0.025, bottom=0, color="red")
p.line(time, speed, legend_label='速度', line_width=2, color="blue")

st.bokeh_chart(p, use_container_width=True)
