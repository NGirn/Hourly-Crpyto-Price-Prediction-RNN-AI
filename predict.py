import pandas as pd
import os
from sklearn import preprocessing
from collections import deque
import random
import numpy as np 
import time
import tensorflow as tf 
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

SEQ_LEN = 240
FUTURE_PERIOD_PREDICT = 4
RATIO_TO_PREDICT = "BTCUSDT"
EPOCHS = 10
BATCH_SIZE = 64
NAME = f"{RATIO_TO_PREDICT}-{SEQ_LEN}-SEQ-{FUTURE_PERIOD_PREDICT}-PRED-{int(time.time())}"


def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0

def preprocess_df(df):
    df = df.drop('future', 1)
    
    for col in df.columns:
        if col != "target":
            df[col] = df[col].pct_change()
            df.dropna(inplace=True)
            df[col] = preprocessing.scale(df[col].values)
    
    df.dropna(inplace=True)

    sequential_data = []
    prev_days = deque(maxlen=SEQ_LEN)
    
    for i in df.values:
        prev_days.append([n for n in i[:-1]])
        if len(prev_days) == SEQ_LEN:
            sequential_data.append([np.array(prev_days), i[-1]])
    
    return np.array(df)

main_df = pd.DataFrame()

ratios = ["ETHUSDT", "BTCUSDT", "LTCUSDT", "NEOUSDT"]
for ratio in ratios:
    dataset = f"crypto_data/{ratio}.csv"

    df = pd.read_csv(dataset, names=["time", "close", "volume"])
    df.rename(columns={"close": f"{ratio}_close", "volume":f"{ratio}_volume"}, inplace=True)

    df.set_index("time", inplace=True)
    df = df[[f"{ratio}_close", f"{ratio}_volume"]]

    if len(main_df) == 0:
        main_df = df
    else:
        main_df = main_df.join(df)

main_df['future'] = main_df[f"{RATIO_TO_PREDICT}_close"].shift(-FUTURE_PERIOD_PREDICT)
main_df['target'] = list(map(classify, main_df[f"{RATIO_TO_PREDICT}_close"], main_df["future"]))

x = preprocess_df(main_df)

model = load_model('BTCUSDT 180 3 60%/RNN_Final-09-0.603.model')

pred = model.predict(x)

print (pred)