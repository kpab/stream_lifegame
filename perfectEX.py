import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
import time
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation

st.title("stream life game")
p = 0.3
csv_files=[]

# for i in range(5):
#     df = pd.read_csv(f"data0{i}.csv", header=None, dtype=str)



class LifeGame:
    def __init__(self, csv_file):
        df = pd.read_csv(csv_file, header=None, dtype=str)
        # 空白消す
        df = df.replace('', np.nan).fillna('0')
        # DataFrameをnumpy
        self.field = df.applymap(lambda x: 1 if x in ['●', '1'] else 0).values
        # 最初と最後の行の0削除
        if np.all(self.field[0] == 0) and np.all(self.field[-1] == 0):
            self.field = self.field[1:-1]
        
        # フィールドのサイズを取得
        self.rows, self.cols = self.field.shape
        
        st.info(f"CSVファイルから読み取ったサイズ: {self.rows}行 x {self.cols}列")
     
    # 生存チェク
    def check(self, y, x):
        cnt = 0
        # 正しい隣接セルのリスト
        neighbors = [(-1, -1), (0, -1), (1, -1),
                     (1, 0), (1, 1), (0, 1),
                     (-1, 1), (-1, 0)]
        for dy, dx in neighbors:
            yy, xx = (y + dy) % self.rows, (x + dx) % self.cols  # グリッドのラップ
            cnt += self.field[yy, xx]
        return cnt

    def evolution(self):
        next_field = np.zeros((self.rows, self.cols), dtype=int)
        for y in range(self.rows):
            for x in range(self.cols):
                n = self.check(y, x)
                s = self.field[y, x]
                if s == 0 and n == 3:
                    next_field[y, x] = 1
                elif s == 1 and 2 <= n <= 3:
                    next_field[y, x] = 1
                else:
                    next_field[y, x] = 0
        self.field = next_field
        return self.field

    def get_field(self):
        return self.field

step = st.number_input("ステップ数", min_value=1, max_value=10000, value=100)
csv_file = st.file_uploader("CSVファイルをアップロード", type="csv")

chk = st.button("start")
if chk:
    cancel=st.button("cancel")

# アニメーションループ
if chk and csv_file is not None:
    # ゲームの初期化
    game = LifeGame(csv_file)
    cmap = ListedColormap(['yellow', 'purple'])

    # プロットの設定
    fig, ax = plt.subplots()
    plt.axis('off')  # 軸を非表示にする

    img = ax.imshow(game.field, cmap=cmap)
    # プレースホルダーの作成
    placeholder = st.empty()

    for _ in range(step):
        while cancel:
            break
        game.evolution()
        img.set_data(game.field)      # 画像データを更新
        placeholder.pyplot(fig)       # プレースホルダー内のプロットを更新           
        time.sleep(0.1)               # アニメーションの速度を制御
elif chk:
    st.error("CSVファイルをアップロードしてください。")


