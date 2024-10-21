import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.colors import ListedColormap

def LifeGame(csv_file, sedai_count):
# データファイルの入力
    data = []
    # 入力ファイル読み込み
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        for line in file:
            line = line.strip().split(',')
            data.append(line)
    ncol = len(data) # 行数の取得
    nrow = len(data[0]) # 列数の取得

    print(f'data:{data}')
    print(f'{ncol}行{nrow}列のデータ！！')
    field_old = np.zeros((ncol, nrow), dtype=int)
    field_new = np.zeros((ncol, nrow), dtype=int)

    ccol = 0
    for lis in data:
        crow = 0
        for i in lis:
            if i == '●':
                field_old[ccol, crow] = 1
            else:
                field_old[ccol, crow] = 0
            crow += 1
        ccol += 1


    print(field_old)
    # 初期描画
    # plt.imshow(field_old)
    
    # plt.show()
    # plt.pause(3)

   
    finish = ""
    while finish != "q":
        # 何世代にわたってシミュレートするか

        for i in sedai_count:
            print(f"{int(i)+1}世代")
            
            field_new = time(field_old, field_new, ncol, nrow)

            print(field_new)
            plt.imshow(field_new)
            plt.show()
            plt.pause(3)
           
            field_old = field_new

        #----------------------------------------
        finish = input('qを入力すると終了します:')
        

def time(old,new,ncol,nrow):
    for cl in range(ncol):
        for rw in range(nrow):
            NW = old[(cl-1)%ncol, (rw-1)%nrow]
            N = old[(cl-1)%ncol, (rw)%nrow]
            NE = old[(cl-1)%ncol, (rw+1)%nrow]
            W = old[cl%ncol, (rw-1)%nrow]
            E = old[cl%ncol, (rw+1)%nrow]
            SW = old[(cl+1)%ncol, (rw-1)%nrow]
            S = old[(cl+1)%ncol, rw%nrow]
            SE = old[(cl+1)%ncol, (rw+1)%nrow]
            Total = sum([NW,N,NE,W,E,SW,S,SE])
            
            if old[cl, rw] == 0:
                if Total == 3:
                    new[cl,rw] = 1
                else:
                    new[cl, rw] = 0
            else:
                if Total == 2 or Total == 3:
                    new[cl, rw] == 1
                else:
                    new[cl, rw] == 0
    return new




sedai_count = st.number_input("何世代にわたってシミュレートしますか？", min_value=1, max_value=10000, value=1000)
csv_file = st.file_uploader("CSVファイルをアップロード", type="csv")
chk = st.button("start")

# アニメーションループ
if chk:
    # ゲームの初期化
    game = LifeGame(csv_file)
    # カスタムカラーマップの定義
    # 0を黄色、1を紫色に設定
    cmap = ListedColormap(['yellow', 'purple'])

    # プロットの設定
    fig, ax = plt.subplots()
    plt.axis('off')  # 軸を非表示にする
    img = ax.imshow(game.field, cmap=cmap, interpolation='nearest')
    # プレースホルダーの作成
    placeholder = st.empty()

    for _ in range(sedai_count):
        game.evolution()
        img.set_data(game.field)      # 画像データを更新
        placeholder.pyplot(fig)       # プレースホルダー内のプロットを更新
        st.snow()                     # オプション: 雪のエフェクトを追加
    time.sleep(0.1)               # アニメーションの速度を制御