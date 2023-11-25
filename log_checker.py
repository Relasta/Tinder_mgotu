import pickle
import pandas as pd
# Проверка логов пользователей по просмотренным фото
# with open('users_state.pickle', 'rb') as f: 
#     print(pickle.load(f))


df_rating = pd.read_csv('./bio_rating.txt', encoding='utf-8', header=None)
df_rating.columns = ['FIO', 'Count', 'Elo']
print(df_rating.sort_values(by='Elo', ascending=False)[df_rating['Count'] != 0.0]['FIO'].head(10).to_list())
