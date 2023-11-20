import pickle
# Проверка логов пользователей по просмотренным фото
with open('users_state.pickle', 'rb') as f: 
    print(pickle.load(f))