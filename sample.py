import matplotlib.pyplot as plt
import numpy as np
import time
from matplotlib.colors import ListedColormap


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


# アニメーションループ
for _ in range(5000):
    game.evolution()
    plt.plot(game.field[0],game.field[1],color="black",marker="s",markersize=10)
    plt.pause(0.1)
    