import numpy as np
import pandas as pd
import os

language = 'vi'
# csv_1_hand = pd.read_csv("csv_1_hand.csv")

offset = 20
imgSize = 300
counter = 0
labels = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "A", "B", "C", "D", "E", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "space", "T", "U", "V", "X", "Y"]
start = -1
maintext = ""
df = ""
if os.path.getsize("csv_1_hand.csv") != 0:
    df = pd.read_csv("csv_1_hand.csv")

empty = np.array([0 for i in range(len(df))])
df.columns = ["r_x_1", "r_y_1", "r_x_2", "r_y_2", "r_x_3", "r_y_3", "r_x_4", "r_y_4", "r_x_5", "r_y_5", "r_x_6", "r_y_6", "r_x_7", "r_y_7", "r_x_8", "r_y_8", "r_x_9", "r_y_9", "r_x_10", "r_y_10", "r_x_11", "r_y_11", "r_x_12", "r_y_12", "r_x_13", "r_y_13", "r_x_14", "r_y_14", "r_x_15", "r_y_15", "r_x_16", "r_y_16", "r_x_17", "r_y_17", "r_x_18", "r_y_18", "r_x_19", "r_y_19", "r_x_20", "r_y_20", "r_x_21", "r_y_21", "target"]
target = df.target.copy()
cols = ["l_x_1", "l_y_1", "l_x_2", "l_y_2", "l_x_3", "l_y_3", "l_x_4", "l_y_4", "l_x_5", "l_y_5", "l_x_6", "l_y_6", "l_x_7", "l_y_7", "l_x_8", "l_y_8", "l_x_9", "l_y_9", "l_x_10", "l_y_10", "l_x_11", "l_y_11", "l_x_12", "l_y_12", "l_x_13", "l_y_13", "l_x_14", "l_y_14", "l_x_15", "l_y_15", "l_x_16", "l_y_16", "l_x_17", "l_y_17", "l_x_18", "l_y_18", "l_x_19", "l_y_19", "l_x_20", "l_y_20", "l_x_21", "l_y_21"]
for i in cols:
    df[i] = empty
df = df.drop("target", axis=1)
df["target"] = target

print(df.head())
# for i in range(len(df)):

#     print(df.columns)

df.to_csv("csv_2_hands.csv", index=False)