from datetime import datetime
import telebot
from code_config import *
import pandas as pd

'''
добавить модель
удалить модель
изменить статус модели
получить модель с id и всей информацией
вывести весь список моделей

добавить пользователя
получить пользователя
проверка на админа
существует ли пользователь
'''


#загрузка и сохранение csv файла
def get_user_list():
    return pd.read_csv('data_users.csv')

def save_user_list(users):
    users.to_csv('data_users.csv', index = None)

def get_models_list():
    return pd.read_csv('data_models.csv')

def save_models_list(models):
    models.to_csv('data_models.csv', index = None)



#операции с пользователями
def user_exist(id):
    users = get_user_list()
    return users['id'].isin([int(id)]).any()

def user_add(id, telegram, info):
    users = get_user_list()
    users.loc[len(users.index)] = [int(id), f'@{telegram}', info, 0]
    users = users.drop_duplicates('id')
    save_user_list(users)
    
def user_get(id):
    if user_exist(id):
        users = get_user_list()
        pos = list(users['id']).index(int(id))
        return users.loc[pos]
    else:
        return [0, '0', '0', 0]
    
def user_is_admin(id):
    if user_exist(id):
        user = user_get(id)
        return user.iloc[-1]
    else:
        return 0


#операции с моделями
def model_add(user, info, path):
    models = get_models_list()
    models.loc[len(models.index)] = [0, 
                                      str(datetime.now())[:16],
                                      '00:00',
                                      user,
                                      info,
                                      path
                                      ]
    save_models_list(models)

def model_delete(id):
    models = get_models_list()
    if len(models) > 0:
        models = models.drop(labels=[id], axis=0)
    save_models_list(models)
    
def model_get(id):
    models = get_models_list()
    for i in range(len(models)):
        if i == int(id):
            return int(id), models.loc[int(id)]
    return 0, [0, '0', '0', 0, '0', '0']

def model_get_status(id):
    id, model = model_get(id)
    return model[0]

def model_set_status(id, status):
    models = get_models_list()
    for i in range(len(models)):
        if i == int(id):
            models['status'][i] = status
            
    save_models_list(models)


def check_ext(filename):
    ext = filename.split('.')[-1]
    if ext in extensions:
        return True
    return False
def download_model(file, filename):
    path = models_folder_path + filename
    with open(path, 'wb') as new_file:
        new_file.write(file)
    return path


def status_to_text(s):
    if s == 0:
        return 'Не начато'
    if s == 1:
        return 'Отклонено'
    if s == 2:
        return 'В процессе'
    if s == 3:
        return 'Завершено'
    return 'Неизвестно'

def text_to_status(s):
    if s == 'Не начато':
        return 0
    if s == 'Отклонено':
        return 1
    if s == 'В процессе':
        return 2
    if s == 'Завершено':
        return 3
    return 0




def wait_message():
    return