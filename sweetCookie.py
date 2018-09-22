#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import time, MSGs
import users
import dataBase
import trafficController

#TODO add a filter for spammers
#TODO add an option to get comments

@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id,'start')
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        users.add_user(message.chat.id)
        print dataBase.check_the_user_in_DB(message)
        trafficController.finished_process(message.chat.id,'start')

@bot.message_handler(commands=['fcode'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id, 'fcode')
    if check == "OK":
        response = users.get_DINING_forgotten_code(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'fcode')

@bot.message_handler(commands=['nextweek'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id, 'nextweek')
    if check == "OK":
        response = users.extract_DINING_next_weeks_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'nextweek')

@bot.message_handler(commands=['thisweek'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id, 'thisweek')
    if check == "OK":
        response = users.extract_DINING_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id,'thisweek')

@bot.message_handler(commands=['ordermeal'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id, 'ordermeal')
    if check == "OK":
        users.order_meal_next_week(message.chat.id)
        trafficController.finished_process(message.chat.id, 'ordermeal')

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id, 'text')
    if check == "OK":
        response = users.process_user_MSG(message.chat.id,message.text)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id, 'text')

@bot.callback_query_handler(func=lambda call: True)
def  test_callback(call):
    if users.know_user(call.from_user.id) == False:
        return

    check = trafficController.check_spam(call.from_user.id, 'CALL')
    if check == "OK":
        print call
        response = users.process_user_call(call.from_user.id,call.data,call)
        if response is not None:
            bot.send_message(call.from_user.id, response)
        trafficController.finished_process(call.from_user.id, 'CALL')


while(True):
    try:
        bot.polling()
    except:
        pass
    time.sleep(2)






