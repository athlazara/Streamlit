import streamlit as st
import pandas as pd

st.title('灵魂潮汐升级道具分配工具')

col1, col2, col3 = st.columns(3)
with col1:
    bar_1 = st.number_input('第1等级所需经验', value=16910, min_value=0, key='d_0')
    bar_2 = st.number_input('第2等级所需经验', value=17660, min_value=0, key='d_0')
    bar_3 = st.number_input('第3等级所需经验', value=18420, min_value=0, key='d_0')
    bar_4 = st.number_input('第4等级所需经验', value=19200, min_value=0, key='d_0')
    bar_5 = st.number_input('第5等级所需经验', value=20000, min_value=0, key='d_0')

bar_list = [bar_1, bar_2, bar_3, bar_4, bar_5]
exp_list = [30, 100, 300, 1000]

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

@st.cache
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

with col2:
    if lines:
        final = lines[0]
        if len(lines)>1:
            for line in lines[1:]:
                if line[-1]<final[-1]:
                    final = line
        final.pop()
        df = pd.DataFrame(final, columns=('道具', '数量'))#[['道具']+[(line[0]) for line in final],['数量']+[line[-1] for line in final]]
        st.dataframe(df.style.set_properties(**{'text-align': 'right'}), width=300, height=620)
    else:
        subheader('无整数消耗路径！')