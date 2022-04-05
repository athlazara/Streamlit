import streamlit as st
from opentrons import containers, instruments, robot

robot.home()
text = robot.commands()
st.title(text)
