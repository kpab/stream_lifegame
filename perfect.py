import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import time
from matplotlib.colors import ListedColormap

st.title("AI禁止")
ROWS = 30
COLS = 50
p = 0.3

class LifeGame:
    def __init__(self):
        # 初期フィールドをランダムに設定
        self.field = np.random.choice([0, 1], size=(ROWS, COLS), p=[1 - p, p])

    def check(self, y, x):
        cnt = 0
        # 正しい隣接セルのリスト
        neighbors = [(-1, -1), (0, -1), (1, -1),
                     (1, 0), (1, 1), (0, 1),
                     (-1, 1), (-1, 0)]
        for dy, dx in neighbors:
            yy, xx = (y + dy) % ROWS, (x + dx) % COLS  # グリッドのラップ
            cnt += self.field[yy, xx]
        return cnt

    def evolution(self):
        next_field = np.zeros((ROWS, COLS), dtype=int)
        for y in range(ROWS):
            for x in range(COLS):
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

# ゲームの初期化
game = LifeGame()

# カスタムカラーマップの定義
# 0を黄色、1を紫色に設定
cmap = ListedColormap(['yellow', 'purple'])

# プロットの設定
fig, ax = plt.subplots()
plt.axis('off')  # 軸を非表示にする
img = ax.imshow(game.field, cmap=cmap, interpolation='nearest')

# プレースホルダーの作成
placeholder = st.empty()

# アニメーションループ
for _ in range(5000):
    game.evolution()
    img.set_data(game.field)      # 画像データを更新
    placeholder.pyplot(fig)       # プレースホルダー内のプロットを更新
    st.snow()                     # オプション: 雪のエフェクトを追加
    time.sleep(0.1)               # アニメーションの速度を制御