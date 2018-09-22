#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot
import time, MSGs
import users
import dataBase
import trafficController
import threading, datetime

#TODO add an option to get feedbacks

@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id,'start')
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        users.add_user(message.chat.id)
        print dataBase.check_the_user_in_DB(message)
        trafficController.finished_process(message.chat.id,'start')

@bot.message_handler(commands=['fcode'])
def COMM_fcode(message):
    check = trafficController.check_spam(message.chat.id, 'fcode')
    if check == "OK":
        response = users.get_DINING_forgotten_code(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'fcode')

@bot.message_handler(commands=['nextweek'])
def COMM_nextweek(message):
    check = trafficController.check_spam(message.chat.id, 'nextweek')
    if check == "OK":
        response = users.extract_DINING_next_weeks_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'nextweek')

@bot.message_handler(commands=['thisweek'])
def COMM_thisweek(message):
    check = trafficController.check_spam(message.chat.id, 'thisweek')
    if check == "OK":
        response = users.extract_DINING_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id,'thisweek')

@bot.message_handler(commands=['ordermeal'])
def COMM_ordermeal(message):
    check = trafficController.check_spam(message.chat.id, 'ordermeal')
    if check == "OK":
        users.order_meal_next_week(message.chat.id)
        trafficController.finished_process(message.chat.id, 'ordermeal')

@bot.message_handler(commands=['feedback'])
def COMM_feedback(message):
    bot.send_message(message.chat.id,MSGs.give_your_feedback)
    users.wait_for_feedback(message.chat.id)


@bot.message_handler(content_types=['text'])
def text_MSG(message):
    response = users.process_user_MSG(message.chat.id,message.text,message)
    if response is not None:
        bot.send_message(message.chat.id,response)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    if users.know_user(call.from_user.id) == False:
        return

    print call
    response = users.process_user_call(call.from_user.id,call.data,call)
    if response is not None:
        bot.send_message(call.from_user.id, response)


#Here are the threads:
RUN_THREAD = True
def MAIN_THR():
    global RUN_THREAD
    while(RUN_THREAD):
        try:
            bot.polling()
        except:
            pass
        time.sleep(2)

#Tuesday is Reserve day
def TUESDAY_ALARM():
    global RUN_THREAD
    while(RUN_THREAD):
        try:
            now = datetime.datetime.utcnow() + datetime.timedelta(hours=3,minutes=30)
            ALARM_TIME = now + datetime.timedelta(days = (1 - now.weekday()) % 7)
            ALARM_TIME = ALARM_TIME.replace(year=ALARM_TIME.year,
                                            month=ALARM_TIME.month,
                                            day = ALARM_TIME.day,
                                            hour=15, minute=00, second=00)
            print (ALARM_TIME - now).total_seconds()
            time.sleep((ALARM_TIME - now).total_seconds())
            # time.sleep(2)
            for tmpUserID in users.users_book.keys():
                print "++=",tmpUserID
                if(users.users_book[tmpUserID]["user"] != None and users.users_book[tmpUserID]["pass"] != None):#if there was some password to get in
                    bot.send_message(tmpUserID,"وقت رزرو شده...",reply_markup = MSGs.reserve_time_markup)
        except:
            pass


main_thread = threading.Thread(target = MAIN_THR)
alarm_thread = threading.Thread(target = TUESDAY_ALARM)

main_thread.start()
alarm_thread.start()

main_thread.join()
alarm_thread.join()

