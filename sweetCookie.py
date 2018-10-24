#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot,feedBack_target_chat
import time, MSGs
import users
import dataBase
import trafficController
import threading, datetime

#TODO fix the fcode for dinner
#TODO clean the files in the repo

@bot.message_handler(commands=['start'])
def send_welcome(message):
    check = trafficController.check_spam(message.chat.id,'start')
    if check == "OK":
        bot.send_message(message.chat.id,MSGs.greetings,reply_markup = MSGs.enter_userpass_markup,parse_mode='HTML')
        users.add_user(message.chat.id)
        print dataBase.check_the_user_in_DB(message)
        users.clear_PLCs(message.chat.id)
        trafficController.finished_process(message.chat.id,'start')

@bot.message_handler(commands=['help'])
def COMM_fcode(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_help')
    if check == "OK":
        response = users.send_commandlist(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'COMM_help')

@bot.message_handler(commands=['fcode'])
def COMM_fcode(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_fcode')
    if check == "OK":
        response = users.forgotten_code(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'COMM_fcode')

@bot.message_handler(commands=['nextweek'])
def COMM_nextweek(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_nextweek')
    if check == "OK":
        response = users.next_week_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id,response)
        trafficController.finished_process(message.chat.id,'COMM_nextweek')

@bot.message_handler(commands=['thisweek'])
def COMM_thisweek(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_thisweek')
    if check == "OK":
        response = users.this_week_data(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id,'COMM_thisweek')

@bot.message_handler(commands=['ordermeal'])
def COMM_ordermeal(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_ordermeal')
    if check == "OK":
        response = users.STARTorder_meal(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'COMM_ordermeal')

@bot.message_handler(commands=['test'])
def COMM_ordermeal(message):
    # check = trafficController.check_spam(message.chat.id, 'COMM_get_pri')
    # if check == "OK":
    #     response = users.STARTget_priority(message.chat.id)
    #     if response is not None:
    #         bot.send_message(message.chat.id, response)
    #     trafficController.finished_process(message.chat.id, 'COMM_get_pri')
    bot.send_message(message.chat.id,"test",reply_markup=MSGs.simple_MAIN_markup)

@bot.message_handler(commands=['feedback'])
def COMM_feedback(message):
    bot.send_message(message.chat.id,MSGs.give_your_feedback)
    users.wait_for_feedback(message.chat.id)

@bot.message_handler(commands=['set_places'])
def test_FUNC(message):
    check = trafficController.check_spam(message.chat.id, 'set_places')
    if check == "OK":
        response = users.extract_DINING_places(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'set_places')

# This command is for the admin:
@bot.message_handler(commands=['respond'])
def COMM_respond(message):
    users.process_respond(message.chat.id)

# @bot.message_handler(commands=['test'])
# def test_FUNC(message):
#     users.extract_DINING_places(message.chat.id)

@bot.message_handler(content_types=['text'])
def text_MSG(message):
    response = users.process_user_MSG(message.chat.id,message.text,message)
    if response is not None:
        bot.send_message(message.chat.id,response)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    if users.know_user(call.from_user.id) == False:
        return

    # print "We have a call..."
    response = users.process_user_call(call.from_user.id,call.data,call)
    # print "response: " + str(response)
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
            ALARM_TIME = now + datetime.timedelta(days = ((7 - now.weekday()) % 7) +1)
            ALARM_TIME = ALARM_TIME.replace(year=ALARM_TIME.year,
                                            month=ALARM_TIME.month,
                                            day = ALARM_TIME.day,
                                            hour=15, minute=00, second=00)
            wait_time = (ALARM_TIME - now).total_seconds() % (7*24*60*60)
            print wait_time
            print (ALARM_TIME - now).total_seconds()
            time.sleep(wait_time)
            # time.sleep(2)
            counter = 0
            for tmpUserID in users.users_book.keys():
                print "++=",tmpUserID
                try:
                    if(users.users_book[tmpUserID]["user"] != None and users.users_book[tmpUserID]["pass"] != None):#if there was some password to get in
                        bot.send_message(tmpUserID,"وقت رزرو شده...",reply_markup = MSGs.reserve_time_markup)
                        counter = counter + 1
                except:
                    pass

            bot.send_message(feedBack_target_chat,"Number of users: " + str(counter))
        except:
            pass


main_thread = threading.Thread(target = MAIN_THR)
alarm_thread = threading.Thread(target = TUESDAY_ALARM)

main_thread.start()
alarm_thread.start()

main_thread.join()
alarm_thread.join()

