import streamlit as st
import pandas as pd

st.title('灵魂潮汐升级道具分配工具')

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        exp_1 = st.checkbox('30点', value=True)
        exp_3 = st.checkbox('300点')
    with col2:
        exp_2 = st.checkbox('100点')
        exp_4 = st.checkbox('1000点')

with st.sidebar:
    select = st.radio("50-55级参数：", ('人物等级参数', '灵蕴等级参数'))
    if select=='人物等级参数':
        bar_list = [16910, 17660, 18420, 19200, 20000]
    else:
        bar_list = [3710, 3860, 4010, 4160, 4320]

with st.sidebar.expander("经验值设定"):
    with st.form("经验值设定"):
        bar_1 = st.number_input('第1等级所需经验', value=bar_list[0], min_value=0, key='d_0')
        bar_2 = st.number_input('第2等级所需经验', value=bar_list[1], min_value=0, key='d_0')
        bar_3 = st.number_input('第3等级所需经验', value=bar_list[2], min_value=0, key='d_0')
        bar_4 = st.number_input('第4等级所需经验', value=bar_list[3], min_value=0, key='d_0')
        bar_5 = st.number_input('第5等级所需经验', value=bar_list[4], min_value=0, key='d_0')
        submitted = st.form_submit_button("设定完成")
        if submitted:
            bar_list = [bar_1, bar_2, bar_3, bar_4, bar_5]

exp_list = []
if exp_1:
    exp_list.append(30)
if exp_2:
    exp_list.append(100)
if exp_3:
    exp_list.append(300)
if exp_4:
    exp_list.append(1000)

#bar_list = [bar_1, bar_2, bar_3, bar_4, bar_5]

def exp_num(bar, red, exp):
    n = 1
    while exp*n < bar-red:
        n+=1
    else:
        rem = exp*n-(bar-red)
    info = [exp, n, rem]
    return info

def dict_grow(bar, red):
    Dict = {}
    for exp in exp_list:
        lv = exp_num(bar, red, exp)
        Dict[str(lv)] = {'red':lv[-1]}
    return Dict

def words_min(words):
    words = words.strip("[")
    words = words.strip("]")
    exp = words.split(',')[0].strip()
    n = words.split(',')[1].strip()
    return [int(exp), int(n)]

Dict = dict_grow(bar_list[0], 0)

for key_1,value_1 in Dict.items():
    red = value_1['red']
    value_1 = dict_grow(bar_list[1], red)
    for key_2,value_2 in value_1.items():
        red = value_2['red']
        value_2 = dict_grow(bar_list[2], red)
        for key_3,value_3 in value_2.items():
            red = value_3['red']
            value_3 = dict_grow(bar_list[3], red)
            for key_4,value_4 in value_3.items():
                red = value_4['red']
                value_4 = dict_grow(bar_list[4], red)
                value_3[key_4] = value_4
            value_2[key_3] = value_3
        value_1[key_2] = value_2
    Dict[key_1] = value_1

lines = []
for key_1,value_1 in Dict.items():
    for key_2,value_2 in value_1.items():
        for key_3,value_3 in value_2.items():
            for key_4,value_4 in value_3.items():
                for key_5,value_5 in value_4.items():
                    if value_5['red']==0:
                        line = [words_min(key_1), words_min(key_2), words_min(key_3), words_min(key_4), words_min(key_5)]
                        min_num = 0
                        for unit in line:
                            if unit[0]==exp_list[0]:
                                min_num+=unit[1]
                        line.append(min_num)
                        lines.append(line)

def choose_min(lines):
    final = lines[0]
    if len(lines)>1:
        for line in lines[1:]:
            if line[-1]<final[-1]:
                final = line
    lines.remove(final)
    df = pd.DataFrame([['Exp']+['%.0f'%unit[0] for unit in final[0:-1]],['Num']+['%.0f'%unit[1] for unit in final[0:-1]]], columns=['','Lv51','Lv52','Lv53','Lv54','Lv55'])
    st.dataframe(df.style.set_properties(**{'text-align': 'center', 'background-color': 'green', 'color': 'white'}), width=1000, height=300)

if lines:
    st.caption('最优路径：')
    copy = lines.copy()
    choose_min(copy)
    if copy:
        choose_min(copy)
        if copy:
            choose_min(copy)
            if copy:
                choose_min(copy)
    st.caption('全局路径：')
    for line in lines:
        line.pop()
    dic = []
    for line in lines:
        dic.append(['Exp']+['<%.0f>'%unit[0] for unit in line])
        dic.append(['Num']+['%.0f'%unit[1] for unit in line])
    df = pd.DataFrame(dic, columns=['','Lv51','Lv52','Lv53','Lv54','Lv55'])
    #df.style.hide_index() 隐藏序号无效
    st.dataframe(df.style.set_properties(**{'text-align': 'center'}), width=1000, height=310)
else:
    '**_无整数消耗路径！_**', :ghost:
