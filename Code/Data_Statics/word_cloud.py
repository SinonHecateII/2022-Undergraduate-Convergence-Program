
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Data_Statics\github_2011_2021(0_1).csv', encoding='cp949')

df['date'] = df['created_at']
df['date'] = df.created_at.str[0:10] # 날짜 부분 추출
df['date'] = pd.to_datetime(df.date)
dt = df.sort_values(by='date')

dt = dt.drop(['created_at'], axis=1)
dt = dt.drop(['updated_at'], axis=1)
dt = dt.drop(['pushed_at'], axis=1)

value = dt.sum()
value = value.drop("year")
value = value.drop("User_ID")
value = value.drop("User_Name")
value = value.drop("Num")
sort_val = value.sort_values(ascending = False)

List_Lang = sort_val.index
List_Lang = List_Lang.to_list()
print(List_Lang)