# Code by jollysoul
import streamlit as st
import random
import numpy as np

r15c1,r15c2,r15c3 = st.columns([6,3,9])
with r15c1:
    r15form = st.form("r15form")
    num_rows = int(r15form.number_input("请输入行数 Input Rows：",1,100,20,1))
    num_cols = int(r15form.number_input("请输入列数 Input Columns：",1,100,20,1))
    if r15form.form_submit_button("画迷宫 Draw Maze"):
        M = np.zeros((num_rows,num_cols,5), dtype=np.uint8)
        image = np.zeros((num_rows*10,num_cols*10), dtype=np.uint8)
        r = 0
        c = 0
        history = [(r,c)]
        while history: 
            M[r,c,4] = 1
            check = []
            if c > 0 and M[r,c-1,4] == 0:
                check.append('L')  
            if r > 0 and M[r-1,c,4] == 0:
                check.append('U')
            if c < num_cols-1 and M[r,c+1,4] == 0:
                check.append('R')
            if r < num_rows-1 and M[r+1,c,4] == 0:
                check.append('D')

            if len(check):
                history.append([r,c])
                move_direction = random.choice(check)
                if move_direction == 'L':
                    M[r,c,0] = 1
                    c = c-1
                    M[r,c,2] = 1
                if move_direction == 'U':
                    M[r,c,1] = 1
                    r = r-1
                    M[r,c,3] = 1
                if move_direction == 'R':
                    M[r,c,2] = 1
                    c = c+1
                    M[r,c,0] = 1
                if move_direction == 'D':
                    M[r,c,3] = 1
                    r = r+1
                    M[r,c,1] = 1
            else:
                r,c = history.pop()
        M[0,0,0] = 1
        M[num_rows-1,num_cols-1,2] = 1
        for row in range(0,num_rows):
            for col in range(0,num_cols):
                cell_data = M[row,col]
                for i in range(10*row+2,10*row+8):
                    image[i,range(10*col+2,10*col+8)] = 255
                if cell_data[0] == 1: 
                    image[range(10*row+2,10*row+8),10*col] = 255
                    image[range(10*row+2,10*row+8),10*col+1] = 255
                if cell_data[1] == 1: 
                    image[10*row,range(10*col+2,10*col+8)] = 255
                    image[10*row+1,range(10*col+2,10*col+8)] = 255
                if cell_data[2] == 1: 
                    image[range(10*row+2,10*row+8),10*col+9] = 255
                    image[range(10*row+2,10*row+8),10*col+8] = 255
                if cell_data[3] == 1: 
                    image[10*row+9,range(10*col+2,10*col+8)] = 255
                    image[10*row+8,range(10*col+2,10*col+8)] = 255
        with r15c3:
            st.image(image,caption=f"{num_rows} x {num_cols} 迷宫")
