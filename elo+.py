from random import randint
import pandas as pd 

df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
df_rating = df.assign(Count=float(0), Elo=float(1000)) 
df_rating['FIO'] = df_rating['Name'] + df_rating['Surname']
df_rating = df_rating[['FIO', 'Count', 'Elo']]

# This is the parameter which makes "wins" more or less important
# In normal chess games this is usually 20
k = 30
l = df.shape[0]
lev = 0
prav = 0
try:
    while True:
        # Get two random elements
        if lev == 0 and prav == 0:
            a = randint(0,l-1)
            b = randint(0,l-1) 
        elif lev != 0:
            b = randint(0,l-1) 
            lev = 0
        elif prav != 0:
            a = randint(0,l-1) 
            pav = 0
        while a == b:
            b = randint(0,l-1)

        # Найти элементы в списке по их id и посчитать их E
        element_a = df_rating.iloc[a].to_list()
        element_b = df_rating.iloc[b].to_list()
        # Это должно происходить внутри фунцкии get_random_num
        R_a = float(element_a[2])
        R_b = float(element_b[2])
        E_a = 1/(1 + (10**((R_b - R_a)/480)))
        E_b = 1/(1 + (10**((R_a - R_b)/480)))
        
        # После выбора <- / ->
        inpt = str(input("Которая лучше?\n[1] "+str(element_a[0])+" or [2] "+str(element_b[0]+'\n')))

        if "1" in inpt:
            lev = 1
            # Calculate Elo if 1 wins
            df_rating.at[a, 'Elo'] = R_a + k*(1-E_a)
            df_rating.at[b, 'Elo'] = R_b + k*(0-E_b)
            # Increment counter
            df_rating.at[a, 'Count'] += 1
            df_rating.at[b, 'Count'] += 1
        elif "2" in inpt:
            prav = 1
            # Calculate elo if 2 wins
            df_rating.at[b, 'Elo'] = R_b + k*(1-E_b)
            df_rating.at[a, 'Elo'] = R_a + k*(0-E_a)
            # Increment counter
            df_rating.at[a, 'Count'] += 1
            df_rating.at[b, 'Count'] += 1


# Остановка кода через - ctrl+c
except KeyboardInterrupt as e:
    print(df_rating.sort_values(by='Elo', ascending=False).head(10)) # Сортировка значений по убывани
    df_rating.to_csv('./bio_rating.txt', header=False, index=False)

# write_string = ''
# # Сортировка по рейтингу сверху вниз
# while list != []:
#     max = [0, 0, 0]
#     for i in list:
#         if max[2] < i[2]:
#             max = i
#     for i in max:
#         write_string += str(i)+", "
#     write_string += "\n"
#     list.remove(max)
# list_file = open(filename, "w", encoding='utf-8')
# list_file.write(write_string)
# list_file.close()
# with open('./bio_rating.txt', "w+", encoding='utf-8') as file:
#     for i in df_rating:    
#         file.write(i)

