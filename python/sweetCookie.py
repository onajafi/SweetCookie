#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from inits import bot,feedBack_target_chat
import time, MSGs
import users
import dataBase
import trafficController
import threading, datetime
import commercial
import Error_Handle


#TODO implement a cancel commad for the reserved meal
#TODO fix the fcode for dinner


@bot.message_handler(commands=['start','restart'])
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

@bot.message_handler(commands=['inc_credit'])
def test_FUNC(message):
    check = trafficController.check_spam(message.chat.id, 'inc_credit')
    if check == "OK":
        response = users.STARTincreasing_credit(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'inc_credit')

@bot.message_handler(commands=['set_auto_res'])
def COMM_set_auto_res(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_get_pri')
    if check == "OK":
        response = users.STARTset_auto_res(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'COMM_get_pri')

@bot.message_handler(commands=['test_auto_res'])
def COMM_test_auto_res(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_test_auto_res')
    if check == "OK":
        response = users.START_comm_to_test_auto_res(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'COMM_test_auto_res')

@bot.message_handler(commands=['cancel_auto_res'])
def COMM_test_auto_res(message):
    check = trafficController.check_spam(message.chat.id, 'COMM_cancel_auto_res')
    if check == "OK":
        response = users.START_comm_cancel_auto_res(message.chat.id)
        if response is not None:
            bot.send_message(message.chat.id, response)
        trafficController.finished_process(message.chat.id, 'COMM_cancel_auto_res')

@bot.message_handler(commands=['test'])
def COMM_ordermeal(message):
    # check = trafficController.check_spam(message.chat.id, 'COMM_get_pri')
    # if check == "OK":
    #     response = users.STARTget_priority(message.chat.id)
    #     if response is not None:
    #         bot.send_message(message.chat.id, response)
    #     trafficController.finished_process(message.chat.id, 'COMM_get_pri')
    # bot.send_message(message.chat.id,"test",reply_markup=MSGs.simple_MAIN_markup)
    # users.test(message.chat.id)
    pass

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

# This command is for the admin:
@bot.message_handler(commands=['broadcast'])
def COMM_broadcast(message):
    users.process_broadcast(message.chat.id)

# This command is for the admin:
@bot.message_handler(commands=['delete_broadcast'])
@Error_Handle.secure_from_exception
def photo_MSG(message):
    if message.from_user.id == feedBack_target_chat:
        commercial.erase_last_30_MSGs(message.chat.id)

@bot.message_handler(commands=['cancel'])
def COMM_cancel(message):
    users.process_cancel(message.chat.id)

@bot.message_handler(content_types=['text'])
def text_MSG(message):
    if users.users_book[message.from_user.id]["state"] == "broadcast_waiting_message":
        print "ITS A simple text message to send"
        print message.json[u'message_id']
        commercial.broadcast_POST(message)
        return
    response = users.process_user_MSG(message.chat.id,message.text,message)
    if response is not None:
        bot.send_message(message.chat.id,response)

@bot.message_handler(content_types=['photo'])
@Error_Handle.secure_from_exception
def photo_MSG(message):
    if users.users_book[message.from_user.id]["state"] == "broadcast_waiting_message":
        print "ITS A PHOTO"
        print message.json[u'message_id']
        commercial.broadcast_POST(message)


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
            print "wait_time: ",wait_time
            print (ALARM_TIME - now).total_seconds()
            time.sleep(wait_time)
            # time.sleep(2)
            auto_res_count = 0
            counter = 0
            for tmpUserID in users.users_book.keys():
                print "++=",tmpUserID
                try:
                    if(tmpUserID not in users.users_auto_res_days.keys()):# Make sure this guy doesn't have an auto_res
                        if(users.users_book[tmpUserID]["user"] != None and users.users_book[tmpUserID]["pass"] != None): # If there was some password to get in
                            bot.send_message(tmpUserID,"وقت رزرو شده...",reply_markup = MSGs.reserve_time_markup)
                            counter += 1
                    else:
                        auto_res_count += 1
                except:
                    pass

            bot.send_message(feedBack_target_chat,"Number of users: " + str(counter+auto_res_count))
            bot.send_message(feedBack_target_chat, "Number of auto_res: " + str(auto_res_count))
            # bot.send_message(feedBack_target_chat, "lunching the AUTO_RESERVE...")
            # AUTO_RESERVE_TRIG()
            # bot.send_message(feedBack_target_chat, "finished AUTO_RESERVE :)")
        except:
            pass

MAX_AUTO_RES_THREAD_NUM = 3
#Do the auto reserve for all of those who have setup the auto_res
def AUTO_RESERVE_TRIG():
    global MAX_AUTO_RES_THREAD_NUM
    thread_queue = []
    for userID in users.users_auto_res_days.keys():
        if(len(users.users_pri_list[userID]) != 0):
            #Make sure there is enough space to make a new thread:
            if(len(thread_queue) >= MAX_AUTO_RES_THREAD_NUM ):
                idx = 0
                while True:
                    THR_elem = thread_queue[idx]
                    if(not THR_elem.isAlive()):
                        THR_elem.join()
                        thread_queue.remove(THR_elem)
                        break
                    idx = (idx + 1) % MAX_AUTO_RES_THREAD_NUM
                    time.sleep(0.1)

            #Fire the new thread
            thread_queue.append(threading.Thread(target=users.START_auto_res_quiet, args=(userID,)))
            thread_queue[-1].start()

    for THR_elem in thread_queue:
        THR_elem.join()


main_thread = threading.Thread(target = MAIN_THR)
alarm_thread = threading.Thread(target = TUESDAY_ALARM)

main_thread.start()
alarm_thread.start()

main_thread.join()
alarm_thread.join()

