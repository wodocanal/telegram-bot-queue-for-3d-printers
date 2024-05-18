import os
import pandas as pd
from code_functions import *

from datetime import datetime

from code_config import *


import telebot
from telebot import TeleBot
from telebot import types

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, '1')
    flag = False
    while not flag:
        try:
            msg = bot.get_updates()
            flag = True
        except:
            pass
    bot.send_message(message.chat.id, msg['message']['text'])


@bot.message_handler(message_type=['text'])
def command(message):
    bot.send_message(message.chat.id, 'хз текст')
    
bot.polling(none_stop = True)