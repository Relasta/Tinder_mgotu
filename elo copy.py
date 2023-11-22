from random import randint
import pandas as pd 

df = pd.read_csv('./bio.txt', encoding='utf-8', header=None)
df.columns = ['Link', 'Surname', 'Name', 'Group', 'Id']
df_rating = df.assign(Count=float(0), Elo=float(1000)) 
df_rating['FIO'] = df_rating['Name'] + df_rating['Surname']
df_rating = df_rating[['FIO', 'Count', 'Elo']]

filename = 'bio_rait_train.txt'
lines = [line.rstrip('\n') for line in open(filename, encoding='utf-8')]

# This is the parameter which makes "wins" more or less important
# In normal chess games this is usually 20
k = 45.0
list = []
for i in lines:
    # Skip line if empty
    if i.strip() == "": 
        continue
    splitted = i.split(",")
    element_name = splitted[0].strip()
    
    if len(splitted) == 1:
        count = 0.0
        elo = 1000.0
    else:
        count = float(splitted[1].strip())
        elo = float(splitted[2].strip())
    i = [element_name, count, elo]
    list.append(i)

l = len(list)
try:
    while True:
        # Get two random elements
        a = randint(0,l-1)
        b = randint(0,l-1) 
        while a == b:
            b = randint(0,l-1)

        # Найти элементы в списке по их id и посчитать их E
        element_a = list[a]
        element_b = list[b]
        # Это должно происходить внутри фунцкии get_random_num
        R_a = element_a[2]
        R_b = element_b[2]
        E_a = 1/(1 + (10**((R_b - R_a)/480)))
        E_b = 1/(1 + (10**((R_a - R_b)/480)))
        
        # После выбора <- / ->
        inpt = str(input("Которая лучше?\n[1] "+str(element_a[0])+" or [2] "+str(element_b[0]+'\n')))

        if "1" in inpt:
            # Calculate Elo if 1 wins
            element_a[2] = R_a + k*(1-E_a)
            element_b[2] = R_b + k*(0-E_b)
            # Increment counter
            element_a[1] += 1
            element_b[1] += 1
        elif "2" in inpt:
            # Calculate elo if 2 wins
            element_b[2] = R_b + k*(1-E_b)
            element_a[2] = R_a + k*(0-E_a)
            # Increment counter
            element_a[1] += 1
            element_b[1] += 1

# Остановка кода через - ctrl+c
except KeyboardInterrupt as e:
    True

write_string = ''
# Сортировка по рейтингу сверху вниз
while list != []:
    max = [0, 0, 0]
    for i in list:
        if max[2] < i[2]:
            max = i
    for i in max:
        write_string += str(i)+", "
    write_string += "\n"
    list.remove(max)
list_file = open(filename, "w", encoding='utf-8')
list_file.write(write_string)
list_file.close()
