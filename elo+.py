
import pandas as pd 

def making_rating(df_rating, a, b, inpt):
    # Найти элементы в списке по их id и посчитать их E
    element_a = df_rating.iloc[a].to_list()
    element_b = df_rating.iloc[b].to_list()
    # Это должно происходить внутри фунцкии get_random_num
    R_a = float(element_a[2])
    R_b = float(element_b[2])
    # Если два элемента еще не сравнивались им присваевается 1000 баллов Elo
    if R_a == float(0.0) and R_b == float(0.0):
        R_a += 1000.0
        R_b += 1000.0
    elif R_a == 0:
        R_a += 1000.0
    elif R_b == 0:
        R_b += 1000.0
    # Нахождение предположительного рейтинга Elo
    E_a = 1/(1 + (10**((R_b - R_a)/480)))
    E_b = 1/(1 + (10**((R_a - R_b)/480)))
    # Ранжировка коэф-та в зависимости от рейтинга
    if R_a < 2100.0:
        k_a = 32
    elif 2100.0 <= R_a <= 2400.0:
        k_a = 24
    elif  k_a > 2400.0:
        k_a = 16
    if R_b < 2100.0:
        k_b = 32
    elif 2100.0 <= R_b <= 2400.0:
        k_b = 24
    elif  k_b > 2400.0:
        k_b = 16

    if 1 == inpt:
        # Calculate Elo if 1 wins
        df_rating.at[a, 'Elo'] = R_a + k_a*(1-E_a)
        df_rating.at[b, 'Elo'] = R_b + k_b*(0-E_b)
        # Increment counter
        df_rating.at[a, 'Count'] += 1
        df_rating.at[b, 'Count'] += 1
        # writing in file
        df_rating.to_csv('./bio_rating.txt', header=False, index=False)
    elif 2 == inpt:
        # Calculate elo if 2 wins
        df_rating.at[b, 'Elo'] = R_b + k_b*(1-E_b)
        df_rating.at[a, 'Elo'] = R_a + k_a*(0-E_a)
        # Increment counter
        df_rating.at[a, 'Count'] += 1
        df_rating.at[b, 'Count'] += 1
        # writing in file
        df_rating.to_csv('./bio_rating.txt', header=False, index=False)

df_rating = pd.read_csv('./bio_rating.txt', encoding='utf-8', header=None)
df_rating.columns = ['FIO', 'Count', 'Elo']
# df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
# df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
# df_rating = df.assign(Count=float(0), Elo=float(0)) 
# df_rating['FIO'] = df_rating['Name'] + df_rating['Surname']
# df_rating = df_rating[['FIO', 'Count', 'Elo']]

print(df_rating.head(3))
making_rating(df_rating, 1, 2, 1)
print(df_rating.head(3))
