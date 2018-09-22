#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import time, MSGs
import users
import dataBase

#TODO add a filter for spammers

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
    users.add_user(message.chat.id)
    print dataBase.check_the_user_in_DB(message)

@bot.message_handler(commands=['fcode'])
def send_welcome(message):
    response = users.get_DINING_forgotten_code(message.chat.id)
    if response is not None:
        bot.send_message(message.chat.id,response)

@bot.message_handler(commands=['nextweek'])
def send_welcome(message):
    response = users.extract_DINING_next_weeks_data(message.chat.id)
    if response is not None:
        bot.send_message(message.chat.id,response)

@bot.message_handler(commands=['thisweek'])
def send_welcome(message):
    response = users.extract_DINING_data(message.chat.id)
    if response is not None:
        bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['ordermeal'])
def send_welcome(message):
    users.order_meal_next_week(message.chat.id)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    response = users.process_user_MSG(message.chat.id,message.text)
    if response is not None:
        bot.send_message(message.chat.id,response)

@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    print call
    response = users.process_user_call(call.from_user.id,call.data,call)
    if response is not None:
        bot.send_message(call.from_user.id, response)

while(True):
    try:
        bot.polling()
    except:
        pass
    time.sleep(2)






