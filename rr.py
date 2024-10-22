import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import time
import pandas as pd
st.title("lifegame")
ROWS=30
COLS=50
p=0.3


class LifeGame():
    def __init__(self):
        self.field=np.random.choice([0,1],[ROWS,COLS],p=[1-p,p])
    def check(self,y,x):
        cnt=0
        tbl=[(-1,-1),(0,-1),(-1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        for t in tbl:
            xx,yy=[x+t[0],y+t[1]]
            if xx==COLS:xx=0
            if yy==ROWS:yy=0
            if self.field[yy][xx]:cnt+=1
        return cnt
    def evolution(self,t=-1):
        if t==0:return self.field
        next_field=np.zeros([ROWS,COLS],dtype=int)
        for y in range(ROWS):
            for x in range(COLS):
                n=self.check(y,x)
                s=self.field[y,x]
                if s==0:
                    if n==3:
                        next_field[y,x]=1
                    else:
                        next_field[y,x]=0
                else:
                    if n<=1 or n>=4:
                        next_field[y,x]=0
                    else:
                        next_field[y,x]=1
        self.field=next_field
        return self.field
L=LifeGame()
with st.empty():
    for t in range(5000):
        field_data=L.evolution(t)
        st.snow()
        # st.write(field_data)
        for i in range(ROWS):
            for j in range(COLS):
                if field_data[i][j]==1:
                    plt.plot(i,j,color="purple",marker="s",markersize=5)
                else:
                    plt.plot(i,j,color="yellow",marker="s",markersize=5)
        st.pyplot(plt)
       
        
        time.sleep(1)