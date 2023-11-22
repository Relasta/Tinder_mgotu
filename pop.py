import pandas as pd
# Подключаемся к файлу с данными
df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
df = df[['Link', 'Name', 'Surname', 'Id']]
df_rating = df.assign(Count=float(0), Elo=float(1000)) 
df_rating['FIO'] = df_rating['Name'] + df_rating['Surname']
df_rating = df_rating[['FIO', 'Count', 'Elo']]
print(df_rating.head())
