import streamlit as st
from opentrons import containers, instruments, robot

robot.head_speed(x=12000, y=12000, z=4000, a=600, b=600)
tuberack1 = containers.load('tube-rack-2ml', 'C1')
tuberack2 = containers.load('tube-rack-2ml', 'D1')
tuberack3 = containers.load('tube-rack-2ml', 'C2')
tuberack4 = containers.load('tube-rack-2ml', 'D2')

containers.create(
    'bottle',             # name of you container
    grid=(1, 1),                   # specify amount of (columns, rows)
    spacing=(60, 60),               # distances (mm) between each (column, row)
    diameter=50,                    # diameter (mm) of each well on the EPplate
    depth=60)                       # depth (mm) of each well on the EPplate
trough = containers.load('bottle','A2') # trough-1row-25ml

p50000 = instruments.Pipette(
        axis="a",
        max_volume=50000,
        min_volume=0,
        channels=1,
        name="p50000"
)

wells = []
wells.extend(tuberack1.wells())
wells.extend(tuberack2.wells())
wells.extend(tuberack3.wells())
wells.extend(tuberack4.wells())
wells = [well.bottom() for well in wells]

p50000.set_speed(dispense=150) #max=1200
while len(wells)>32:
    p50000.aspirate(50000, trough.wells('A1'))
    p50000.delay(2) #延时3秒
    p50000.dispense(1000, trough.wells('A1').top(-40))
    for well in wells[0:32]:
        p50000.dispense(1500, well)
    p50000.blow_out(trough.wells('A1').top(-40))
    del wells[0:32]
if len(wells)<=32 and len(wells)>0:
    p50000.aspirate(1500*len(wells)+2000, trough.wells('A1'))
    p50000.delay(3) #延时3秒
    p50000.dispense(1000, trough.wells('A1').top(-40))
    for well in wells:
        p50000.dispense(1500, well)
    p50000.blow_out(trough.wells('A1').top(-40))

p50000.set_speed(dispense=600)
p50000.mix(1, 2500, trough.wells('A1').top(-40))

robot.home()
robot.commands()
st.title('运行完毕')
