import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("DB\Git_Data(range(1~50,000)).csv", low_memory=False, encoding='cp949')

df['date'] = df['created_at']
df['year'] = df['created_at']
df['date'] = df.created_at.str[0:10] # 날짜 부분 추출
df['year'] = df.created_at.str[0:4]

df['date'] = pd.to_datetime(df.date)
dt = df.sort_values(by='date')

dt = dt.drop(['created_at'], axis=1)
dt = dt.drop(['updated_at'], axis=1)
dt = dt.drop(['pushed_at'], axis=1)

value = dt.sum()
value = value.drop("User_Name")
value = value.drop("Repository_Name")
value = value.drop("year")
sort_val = value.sort_values(ascending = False)
sort_val = sort_val.drop("Num")
sort_val = sort_val.drop("User_ID")

List_Lang = sort_val.index
List_Lang = List_Lang.to_list()

def list_Chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

list_Chunked = list_Chunk(List_Lang, 10)

List_top10 = list_Chunked[0]

grouped = dt[List_top10].groupby(dt['year']).sum()

grouped.plot(kind='line')
plt.show()