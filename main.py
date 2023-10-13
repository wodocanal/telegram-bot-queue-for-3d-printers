from config import *
#файл id.txt не трогать если есть хоть одна модель в очереди

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start_welcome(message):
    bot.send_message(message.chat.id, 'Для получения списка команд и дополнительной информации воспользуйся командой /help.')
    with open('users.json', 'r', encoding='utf-8') as users_list:
        users = json.load(users_list)
        if str(message.chat.id) not in users.keys():
            users[str(message.chat.id)] = ['@' + message.chat.username, "user"]
    with open("users.json", "w", encoding='utf-8') as users_list:
        json.dump(users, users_list)
    
    
@bot.message_handler(commands=['help'])
def help(message):
    with open('users.json', 'r', encoding='utf-8') as users_list:
        users = json.load(users_list)
    if users[str(message.chat.id)][1] == 'admin':
        bot.send_message(message.chat.id, 'СПИСОК КОМАНД \n /help - отобразить список команд. \n /add - добавить модель в очередь. (Отправляете отдельно команду, затем файл модели, потом комментарий) \n /list - показать очередь. \n /get [номер] - получить модель под нужным номером. \n /set [номер] [новый статус] - поставить статус для модели под нужным номером. \n /del [номер] - удалить модель под нужным номером.')
        bot.send_message(message.chat.id, 'Номер модели можно узнать из первого столбца очереди.')
    else:
        bot.send_message(message.chat.id, 'СПИСОК КОМАНД \n /help - отобразить список команд. \n /add - добавить модель в очередь. (Отправляете отдельно команду, затем файл модели, потом комментарий) \n /list - показать очередь. \n /cancel [номер] - удалить модель из очереди(сработает только если модель была отправлена тобой.)')


@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.send_message(message.chat.id, 'Отправь в этот чат модель, название файла болжно быть в формате [Фамилия_номер класса_название модели], поддерживаются файлы с расширением (stl, stp, step, 3mf, m3d, gcode, a3d).')
    bot.register_next_step_handler(msg, take_file)


def take_file(message):
    try:
        flag = True
        for i in EXTNESIONS:
            if message.document.file_name.endswith(i):
                flag = False
        if flag:
            bot.reply_to(message, 'Не удалось сохранить, пожалуйста отправь файл в одном из доступных форматов(stl, stp, step, 3mf, m3d, gcode, a3d).')
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        global src, filename
        filename = message.document.file_name
        src = DOWNLOAD_DIR + filename
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.reply_to(message, "Успешно сохранено.")
        msg = bot.send_message(message.chat.id, 'Напиши описание модели и комментарий к печати (цвет пластика, количество печатей, желаемое заполнение, срок к которому должна быть готова печать), если комментарий отсутсвует, то отправь слово нет.')
        
        bot.register_next_step_handler(msg, take_info)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка: \n" + str(e) + "\nОтправь другой файл.")


def take_info(message):
    bot.send_message(message.chat.id, "Описание принято, модель поставлена в очередь, жди.")
    model_id = int(open('id.txt', 'r').read())
    
    with open('models.json', 'r', encoding='utf-8') as models_list:
        models = json.load(models_list)
        models[model_id] = [filename, str(datetime.now())[:-10], '@' + message.chat.username, DEFAULT_STATUS, message.text, src]
    with open("models.json", "w", encoding='utf-8') as models_list:
        json.dump(models, models_list, ensure_ascii=False)
        
    model_id+=1
    file = open('id.txt', 'w')
    file.write(str(model_id))
    file.close()
    

@bot.message_handler(commands=['list'])
def show_list(message):
    with open('models.json', 'r', encoding='utf-8') as models_list:
        models = json.load(models_list)
    if len(models) == 0:
        bot.send_message(message.chat.id, "Список пуст.")
        return
    for i in models:
        bot.send_message(message.chat.id, '№' + i + ' | ' + models[i][0] + ' | ' + models[i][1] + ' | ' + models[i][2] + ' | ' + models[i][3] + '.\n')


@bot.message_handler(commands=['get'])
def get(message):
    with open("users.json", "r", encoding='utf-8') as users_list:
        users = json.load(users_list)
        if users[str(message.chat.id)][1] != 'admin':
            bot.send_message(message.chat.id, "У тебя нет прав для выполнения данной команды.")
            return
            
    try:
        number = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Неверный формат команды.")
        return
    
    with open("models.json", "r", encoding='utf-8') as models_list:
        models = json.load(models_list)
    try:
        bot.send_message(message.chat.id, "№" + number + '\nНазвание модели: ' + models[number][0] + '\nДата и время отправления: ' + models[number][1] + '\nОтправитель: ' + models[number][2] + '\nСтатус модели: ' + models[number][3] + '\nОписание модели и комментарий отправителя: '+ models[number][4])                  #успешно
        bot.send_document(message.chat.id, open(models[number][-1], 'rb'))
    except:
        bot.send_message(message.chat.id, "Модели под таким номером не существует")
        return
    

@bot.message_handler(commands=['set'])
def set_status(message):
    with open("users.json", "r", encoding='utf-8') as users_list:
        users = json.load(users_list)
        if users[str(message.chat.id)][1] != 'admin':
            bot.send_message(message.chat.id, "У тебя нет прав для выполнения данной команды.")
            return
    
    try:
        number, text = message.text.split()[1:]
    except:
        bot.send_message(message.chat.id, "Неверный формат команды.")
        return
                
    with open("models.json", "r", encoding='utf-8') as models_list:
        models = json.load(models_list)
    try:
        models[number][3] = text
    except:
        bot.send_message(message.chat.id, "Модели с данным номером не существует.")
        return
    with open("models.json", "w", encoding='utf-8') as models_list:
        json.dump(models, models_list, ensure_ascii=False)
    bot.send_message(message.chat.id, f"Статус модели №{number} успешно изменен.")
    

@bot.message_handler(commands=["del"])
def delete(message):
    with open("users.json", "r", encoding='utf-8') as users_list:
        users = json.load(users_list)
        if users[str(message.chat.id)][1] != 'admin':
            bot.send_message(message.chat.id, "У тебя нет прав для выполнения данной команды.")
            return
        
    try:
        number = message.text.split()[1]
    except:
        bot.send_message(message.chat.id, "Неверный формат команды.")
        return
    with open("models.json", "r", encoding='utf-8') as models_list:
        models = json.load(models_list)

    try: 
        models.pop(number)
        with open("models.json", "w", encoding='utf-8') as models_list:
            json.dump(models, models_list, ensure_ascii=False)
        bot.send_message(message.chat.id, "Успешно удалено")
        
    except Exception as e:
        bot.send_message(message.chat.id, "Модели с данным номером не существует.")
   

@bot.message_handler(commands=["cancel"])
def cancel(message):
    try:
        number = message.text.split()[1] 
    except:
        bot.send_message(message.chat.id, "Неверный формат команды.")
        return

    with open("models.json", "r", encoding='utf-8') as models_list:
        models = json.load(models_list)
    try: 
        if models[number][2] == '@' + message.chat.username:
            if models[number][3] == DEFAULT_STATUS:
                models.pop(number)
                with open("models.json", "w", encoding='utf-8') as models_list:
                    json.dump(models, models_list, ensure_ascii=False)
            else:
                bot.send_message(message.chat.id, "С этой моделью уже начали работу, невозможно удалить.")
                return
            bot.send_message(message.chat.id, "Успешно удалено")
        else:
            bot.send_message(message.chat.id, "У тебя нет прав на удаление данной модели.")
    except:
        bot.send_message(message.chat.id, "Модели с данным номером не существует.")
        
 
#bot.polling(none_stop=True, interval=0)
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print("ПЕРЕПОДКЛЮЧЕНИЕ ", str(e))