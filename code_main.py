from code_functions import *
from code_config import *

import telebot
from telebot import TeleBot
from telebot import types

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def command_start_1(message):
    if not user_exist(message.chat.id):
        msg = bot.send_message(message.chat.id, START_TEXT_1)
        bot.register_next_step_handler(msg, command_start_2)
    else:
        bot.send_message(message.chat.id, START_TEXT_2)
        command_main_menu(message)

def command_start_2(message):
    user_add(message.chat.id, message.from_user.username, message.text)
    bot.send_message(message.chat.id, START_TEXT_3)
    command_main_menu(message)




def command_main_menu(message): #главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(MAIN_MENU_BUTTON_1), types.KeyboardButton(MAIN_MENU_BUTTON_2))
    markup.add(types.KeyboardButton(MAIN_MENU_BUTTON_3), types.KeyboardButton(MAIN_MENU_BUTTON_4))
    
    msg = bot.send_message(message.chat.id, MAIN_MENU_TEXT, reply_markup=markup)
    bot.register_next_step_handler(msg, command_choise)

def command_choise(message):
    if message.text == '/menu':
        return command_main_menu(message)
    if message.text == '/list':
        return command_show_list(message)
    
    match message.text:
        case "Добавить модель":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton(TEXT_BACK))
            msg = bot.send_message(message.chat.id, CHOISE_TEXT_1, reply_markup=markup)
            bot.register_next_step_handler(msg, command_add_model_1)

        case "Посмотреть очередь":
            msg = bot.send_message(message.chat.id, CHOISE_TEXT_2)
            command_show_list(message)

        case "журнал ремонта \n(в разработке)":
            msg = bot.send_message(message.chat.id, CHOISE_TEXT_3)
            command_main_menu(message)

        case "получить конфиг PrusaSlicer \n(в разработке)":
            msg = bot.send_message(message.chat.id, CHOISE_TEXT_3)
            command_main_menu(message)

        case _:
            msg = bot.send_message(message.chat.id, CHOISE_TEXT_4)
            command_main_menu(message)

@bot.message_handler(commands=['menu'])
def command_main_menu_2(message):
    return command_main_menu(message)




def command_add_model_1(message):
    try:
        if check_ext(message.document.file_name):
            model = bot.download_file(bot.get_file(message.document.file_id).file_path)
            path = download_model(model, message.document.file_name)

            bot.reply_to(message, ADD_TEXT_1)
            msg = bot.send_message(message.chat.id, ADD_TEXT_2)
            
            bot.register_next_step_handler(msg, command_add_model_2, path)
        
        else:
            bot.send_message(message.chat.id, ADD_TEXT_3)
            command_main_menu(message)

    except:
        if message.text != TEXT_BACK:
            bot.reply_to(message, ADD_TEXT_4)
        command_main_menu(message)

def command_add_model_2(message, path):
    if message.text != TEXT_BACK:
        model_add(message.chat.id, message.text, path)
        bot.send_message(message.chat.id, ADD_TEXT_1)
    command_main_menu(message)




def command_show_list(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(TEXT_BACK))
    if user_is_admin(message.chat.id):
        markup.add(types.KeyboardButton(TEXT_GET_1))
        
    models = get_models_list()
    
    text = ''
    for i in range(len(models)):
        text += str(i)
        text += ' | '
        text += models['path'][i].split('\\')[-1]
        text += '\n'
        text += models['time'][i]
        text += ' | '
        text += models['printing_time'][i]
        text += ' | '
        text += user_get(int(models['user'][i]))['telegram']
        text += '\n'
    
    
    msg = bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(msg, command_list_choise)

def command_list_choise(message):
    if message.text == 'назад':
        return command_main_menu(message)
    if message.text == '/menu':
        return command_main_menu(message)
    if message.text == '/list':
        return command_show_list(message)
    if message.text == '/start':
        bot.send_message(message.chat.id, 'зачем ты это сделал')
        return command_show_list(message)
    
    if user_is_admin(message.chat.id) and message.text == 'получить модель':
        msg = bot.send_message(message.chat.id, TEXT_GET_2)
        bot.register_next_step_handler(msg, command_get_model)
    else:
        bot.send_message(message.chat.id, 'доступно только для админов')

@bot.message_handler(commands=['list'])
def command_show_list_2(message):
    return command_show_list(message)




def command_get_model(message):
    if not user_is_admin(message.chat.id):
        bot.send_message(message.chat.id, 'недостаточно прав для выполнения данной операции')
        return command_main_menu(message)
        
    if message.text and message.text.isdigit():
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('удалить модель'),
                   types.KeyboardButton('изменить статус модели'))
        
        markup.add(types.KeyboardButton('к очереди'),
                   types.KeyboardButton('в меню'))
        
        
        id, model = model_get(message.text)
        
        text = ''
        text += model['path'].split('\\')[-1]
        text += '\n'
        text+= f'Позиция в очереди: {id}'
        text += '\n'
        text+= f'Время отправки: {model['time']}'
        text += '\n'
        text+= f'Предполагаемое время печати: {model['printing_time']}'
        text += '\n'
        text+= f'Отправлено пользователем: {user_get(model['user'])['telegram']}'
        text += '\n'
        text+= f'Статус модели: {status_to_text(model['status'])}'
        text += '\n'
        text+= f'Дополнительные пожелания: {model['info']}'
        
        
        msg = bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.send_document(message.chat.id, open(model['path'], 'rb'))
        bot.register_next_step_handler(msg, command_get_choise, id)
    else:
        bot.send_message(message.chat.id, 'модели с таким id не обнаружено')
        command_main_menu(message)

def command_get_choise(message, id):
    text = message.text
    if text == 'в меню':
        return command_main_menu(message)
    
    if text == 'к очереди':
        return command_show_list(message)
    
    if text == 'изменить статус модели':
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Не начато'), types.KeyboardButton('Отклонено'))
        markup.add(types.KeyboardButton('В процессе'), types.KeyboardButton('Завершено'))
        markup.add(types.KeyboardButton('Назад'))
        
        msg = bot.send_message(message.chat.id, 'выбери новый статус для этой модели', reply_markup=markup)
        bot.register_next_step_handler(msg, command_change_status, id)
        return
    
    if text == 'удалить модель':
        model_delete(id)
        bot.send_message(message.chat.id, 'модель удалена')
        command_main_menu(message)
        
    else:
        bot.send_message(message.chat.id, 'такой команды нет')
        command_main_menu(message)
        


def command_change_status(message, id):
    if message.text != 'Назад':
        new_status = text_to_status(message.text)
        
        model_set_status(id, new_status)
        model = model_get(id)[1]
        user = model['user'] 

        bot.send_message(message.chat.id, 'статус был изменен')
        bot.send_message(user, f'статус твоей модели был изменен на "{status_to_text(new_status)}" пользователем {user_get(message.chat.id)['telegram']}')
        return command_show_list(message)   
    else:
        return command_show_list(message)




bot.polling(none_stop=True)