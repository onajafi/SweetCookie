#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import operator

import MSGs,scriptCaller,local_time
import trafficController
from inits import bot,feedBack_target_chat
from emoji import emojize
import dataBase
from telebot import types
import Error_Handle
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

users_book = dataBase.get_users_book_from_database() # maps to a Dictionary
users_PLCs = dataBase.get_users_PLCs_from_database() # maps to a Dictionary
users_selected_PLCs = dataBase.get_users_selected_PLCs() # maps to a List
print "initial vals:"
print users_PLCs
print users_selected_PLCs
#TODO check the functions that need the PLCnum to be added

user_meal_menu = {}
user_order_list = {}
tmp_resp_ID = -1

call_PLC_pattern = re.compile("^PLC_[0-9]{1,2}$")
call_NEXT_WEEK_pattern = re.compile("^NEXT_WEEK_[0-9]{1,2}$")
call_THIS_WEEK_pattern = re.compile("^THIS_WEEK_[0-9]{1,2}$")
call_FCODE_pattern = re.compile("^FCODE_[0-9]{1,2}$")
call_ORDER_NEXT_WEEK_pattern = re.compile("^ORDER_NEXT_WEEK_[0-9]{1,2}$")

def add_user(userID):
    try:
        if(userID not in users_book.keys()):
            users_book[userID] = {"user": None, "pass":None, "state":None}
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.add_user")
        return

#Clear places both in memory and database
def clear_PLCs(userID):
    try:
        users_PLCs[userID] = {}
        users_selected_PLCs[userID] = []
        dataBase.update_PLC_database(userID,users_PLCs[userID],users_selected_PLCs[userID])
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.clear_PLCs")
        return

def know_user(userID):
    try:
        if (userID not in users_book.keys()):
            return False
        return True
    except:
        Error_Handle.log_error("ERROR: users.know_user")
        return False

def process_respond(userID):
    if(userID == feedBack_target_chat):
        users_book[userID]["state"] = "respond_waiting_for_ID"
        bot.send_message(userID,"Give the target chat ID:")

def process_user_MSG(userID, message_TXT,message):
    global tmp_resp_ID
    try:
        if(users_book[userID]["state"] == "GetUser"):
            users_book[userID]["user"] = message_TXT
            users_book[userID]["state"] = "GetPass"
            return MSGs.give_pass
        elif(users_book[userID]["state"] == "GetPass"):
            check = trafficController.check_spam(userID, "SCRIPT")
            if check == "OK":
                users_book[userID]["pass"] = message_TXT
                users_book[userID]["state"] = None
                tmp_MSG = extract_DINING_places(userID)
                trafficController.finished_process(userID, "SCRIPT")
                return tmp_MSG
        elif(users_book[userID]["state"] == "FeedBack"):
            bot.forward_message(feedBack_target_chat,userID,message.message_id)
            bot.send_message(feedBack_target_chat,"The users ID is: " + '\n' + str(userID))
            bot.send_message(userID,MSGs.feedBack_sent)
            users_book[userID]["state"] = None
            return
        elif(userID == feedBack_target_chat and users_book[userID]["state"] == "respond_waiting_for_ID"):
            tmp_resp_ID = int(message_TXT)
            bot.send_message(feedBack_target_chat,"Leave your message:")
            users_book[userID]["state"] = "respond_waiting_for_MSG"
        elif(userID == feedBack_target_chat and users_book[userID]["state"] == "respond_waiting_for_MSG"):
            bot.send_message(tmp_resp_ID,message_TXT)
            bot.send_message(feedBack_target_chat, "Sent :)")
            users_book[userID]["state"] = None
        elif(message_TXT == emojize('رزرو هفته بعد:telephone:', use_aliases=True)): # just like /ordermeal
            check = trafficController.check_spam(userID, 'COMM_ordermeal')
            if check == "OK":
                response = STARTorder_meal(userID)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'COMM_ordermeal')
        elif(message_TXT == emojize('نمایش هفته جاری:chart_with_downwards_trend:', use_aliases=True)): # just like /thisweek
            check = trafficController.check_spam(userID, 'COMM_thisweek')
            if check == "OK":
                response = this_week_data(userID)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'COMM_thisweek')
        elif(message_TXT == emojize('دریافت کد فراموشی:u6307:', use_aliases=True)): # just like /fcode
            check = trafficController.check_spam(userID, 'COMM_fcode')
            if check == "OK":
                response = forgotten_code(userID)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'COMM_fcode')
        elif(message_TXT == emojize('لیست دستورات:ledger:', use_aliases=True)):
            check = trafficController.check_spam(userID, 'COMM_help')
            if check == "OK":
                response = send_commandlist(userID)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'COMM_help')
        else:
            pass
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.process_user_MSG")
        users_book[userID]["state"] == None
        return


def process_user_call(userID,call_TXT,ACT_call):
    global users_selected_PLCs
    global users_PLCs
    try:
        print "STEP->1"
        if (call_TXT == "UserPass"):
            check = trafficController.check_spam(userID, "CALL_UserPass")
            if check == "OK":
                users_book[userID]["state"] = "GetUser"
                dataBase.update_UserPass(userID,None,None)
                trafficController.finished_process(userID, "CALL_UserPass")
                return MSGs.give_user
        elif (call_TXT == "OrderNextWeek"):#TODO
            check = trafficController.check_spam(userID, 'COMM_ordermeal')
            if check == "OK":
                STARTorder_meal(userID)
                trafficController.finished_process(userID, 'COMM_ordermeal')
        elif(call_TXT == "FCode"):#Forgotten Code
            if(users_book[userID]["user"] != None and users_book[userID]["pass"] != None):
                check = trafficController.check_spam(userID, "CALL_FCode")
                if check == "OK":
                    tmp_MSG = forgotten_code(userID)
                    trafficController.finished_process(userID, "CALL_FCode")
                    return tmp_MSG
            else:
                bot.send_message(userID,MSGs.please_enter_your_UserPass,reply_markup=MSGs.enter_userpass_markup)
                return

        elif(users_book[userID]["state"] in range(1,8) and call_TXT in ("0","1","2","3","nevermind")):

            if(call_TXT == "nevermind"):
                appending_ans = "چیزی نمی‌خوام"
            else:
                appending_ans = user_meal_menu[userID][users_book[userID]["state"] - 1]["lunch_arr"][int(call_TXT)]["meal_name"]

            bot.edit_message_text(text = ACT_call.message.text +"\n" + appending_ans,
                                  chat_id = userID,
                                  message_id = ACT_call.message.message_id,
                                  reply_markup = None)
            user_order_list[userID][users_book[userID]["state"] - 1] = call_TXT

            check = trafficController.check_spam(userID, "SCRIPT")
            if check == "OK":
                ask_to_choose_meal(userID)
                trafficController.finished_process(userID, "SCRIPT")

        elif (users_book[userID]["state"] in range(8, 15) and call_TXT in ("0", "1", "2", "3", "nevermind")):

            if (call_TXT == "nevermind"):
                appending_ans = "چیزی نمی‌خوام"
            else:
                appending_ans = user_meal_menu[userID][users_book[userID]["state"] - 8]["dinner_arr"][int(call_TXT)][
                    "meal_name"]

            bot.edit_message_text(text=ACT_call.message.text + "\n" + appending_ans,
                                  chat_id=userID,
                                  message_id=ACT_call.message.message_id,
                                  reply_markup=None)
            user_order_list[userID][users_book[userID]["state"] - 1] = call_TXT

            check = trafficController.check_spam(userID, "SCRIPT")
            if check == "OK":
                ask_to_choose_meal(userID)
                trafficController.finished_process(userID, "SCRIPT")

        elif(call_PLC_pattern.match(call_TXT)): # if it matches something like "PLC_19"
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)
            print "::::"
            print users_PLCs
            if(PLC_number in users_selected_PLCs[userID]):# the user wants to cancel this place
                users_selected_PLCs[userID].remove(PLC_number)
                # print "REMOVED"
            else:
                users_selected_PLCs[userID].append(PLC_number)

            print users_PLCs
            print "::::"

            temp_PLC = users_PLCs[userID]
            temp_selected_PLCs = users_selected_PLCs[userID]

            # Saving to the database
            dataBase.update_PLC_database(userID, temp_PLC, temp_selected_PLCs)
            # The users_selected_PLCs is already up-to-date

            PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            for elem in sorted(temp_PLC.keys()):
                if elem in temp_selected_PLCs:
                    emoji_check = '✅'
                else:
                    emoji_check = '❌'
                PLCs_markup.add(
                    types.InlineKeyboardButton(emojize(emoji_check + temp_PLC[elem]), callback_data="PLC_" + elem))
            PLCs_markup.add(types.InlineKeyboardButton("تموم", callback_data="PLC_DONE"))
            bot.edit_message_reply_markup(userID,ACT_call.message.message_id,reply_markup=PLCs_markup)

        elif(call_TXT == "PLC_DONE"):
            temp_PLC = users_PLCs[userID]
            temp_selected_PLCs = users_selected_PLCs[userID]

            if(temp_selected_PLCs):#If it's not NULL
                temp_MSG = "مکان‌های انتخاب شده برای تحویل وعده غذایی:"
                temp_MSG += '\n'
                for elem in sorted(temp_PLC.keys()):
                    if elem in temp_selected_PLCs:
                        temp_MSG += emojize('✅' + temp_PLC[elem])
                        temp_MSG += '\n'
            else:
                temp_MSG = "جایی برای تحویل وعده انتخاب نشده... :("

            bot.edit_message_text(temp_MSG,userID,ACT_call.message.message_id, reply_markup=MSGs.none_markup)
            bot.send_message(userID,MSGs.lets_start,reply_markup = MSGs.simple_MAIN_markup)

        elif(call_NEXT_WEEK_pattern.match(call_TXT)):
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)
            check = trafficController.check_spam(userID, 'nextweek')
            if check == "OK":
                response = extract_DINING_next_weeks_data(userID,PLC_number)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'nextweek')

        elif(call_THIS_WEEK_pattern.match(call_TXT)):
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)
            check = trafficController.check_spam(userID, 'thisweek')
            if check == "OK":
                response = extract_DINING_data(userID,
                                               PLC_number)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'thisweek')

        elif(call_FCODE_pattern.match(call_TXT)):
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)
            check = trafficController.check_spam(userID, 'fcode')
            if check == "OK":
                response = get_DINING_forgotten_code(userID,
                                               PLC_number)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'fcode')

        elif(call_ORDER_NEXT_WEEK_pattern.match(call_TXT)):
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)
            check = trafficController.check_spam(userID, 'ordermeal')
            if check == "OK":
                response = order_meal_next_week(userID,
                                                     PLC_number)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'ordermeal')

        else:
            print "STEP->3"
            bot.send_message(userID, "Don't know what you called!?!?!?\n" + str(users_book[userID]["state"]) + '\n' + call_TXT)
            pass
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.process_user_call")
        return


def update_DINING_UserPass(userID,username_DINING,password_DINING):
    try:
        users_book[userID]["user"] = username_DINING
        users_book[userID]["pass"] = password_DINING
        dataBase.update_UserPass(userID,username_DINING,password_DINING)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.update_DINING_UserPass")
        return


def send_commandlist(userID):
    try:
        bot.send_message(userID, MSGs.how_to_use)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.send_commandlist")
        return


def forgotten_code(userID):
    try:
        selected_PLCs = get_selected_PLCs(userID)

        if(len(selected_PLCs)>1):#It's not empty
            tmp_PLCs = users_PLCs[userID]
            PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            for elem in selected_PLCs:
                PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="FCODE_"+ elem))

            bot.send_message(userID, MSGs.select_PLC,reply_markup = PLCs_markup)
        elif (len(selected_PLCs) == 1):
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'fcode')
            if check == "OK":
                response = get_DINING_forgotten_code(userID,
                                               selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'fcode')
        else:
            bot.send_message(userID, MSGs.no_selected_PLCs)

    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.forgotten_code")
        return
def get_DINING_forgotten_code(userID,PLCnum):
    try:
        meal_type = ""
        if(local_time.IsDinnerTime()):
            meal_type = "شام"
        else:
            meal_type = "ناهار"

        attempts = 1
        while attempts <= 3:
            bot.send_message(userID,"در حال دریافت کد فراموشی وعده " + meal_type)
            temp_data = scriptCaller.get_user_DINING_forgotten_code(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID,
                                                          PLCnum)#TODO add this option to give the dinner OR lunch
            print temp_data
            if(temp_data == None):
                bot.send_message(userID,MSGs.we_cant_do_it_now)
                return
            if (temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID, MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if (temp_data["PASSWORD_STATE"] == "WRONG"):
            return MSGs.your_password_is_wrong

        if("FCode" not in temp_data.keys()):
            bot.send_message(userID, MSGs.we_cant_do_it_now)
            return

        message_TXT = ""
        message_TXT += "کد فراموشی: \n" + str(temp_data["FCode"])

        return message_TXT
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.get_DINING_forgotten_code")
        return


def this_week_data(userID):
    try:
        selected_PLCs = get_selected_PLCs(userID)

        if(len(selected_PLCs)>1):#It's not empty
            tmp_PLCs = users_PLCs[userID]
            PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            for elem in selected_PLCs:
                PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="THIS_WEEK_"+ elem))

            bot.send_message(userID, MSGs.select_PLC,reply_markup = PLCs_markup)
        elif (len(selected_PLCs) == 1):
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'thisweek')
            if check == "OK":
                response = extract_DINING_data(userID,
                                               selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'thisweek')
        else:
            bot.send_message(userID, MSGs.no_selected_PLCs)

    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.this_week_data")
        return
def extract_DINING_data(userID,PLCnum):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID,MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user_DINING_data(users_book[userID]["user"],
                                              users_book[userID]["pass"],
                                              userID,
                                              PLCnum)
            print temp_data
            if (temp_data == None):
                bot.send_message(userID, MSGs.we_cant_do_it_now)
                return
            if(temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID,MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if(temp_data["PASSWORD_STATE"] == "WRONG"):
            bot.send_message(userID,MSGs.your_password_is_wrong,reply_markup = MSGs.enter_userpass_markup)
            return
        else:
            dataBase.update_UserPass(userID, users_book[userID]["user"], users_book[userID]["pass"])

        message_TXT = ""
        message_TXT += "موجودی: \n" + str('%.3f' % temp_data["Balance"]) + '\n'
        if (float(temp_data["Balance"]) < -10):
            message_TXT += emojize("❗اعتبارت کمه، یکم بیشترش کن❗️")
        bot.send_message(userID,message_TXT)

        message_TXT = ""
        bot.send_message(userID, "هفته جاری:")
        for row in temp_data["COMPLETE_TABLE"]:
            message_TXT += "==================\n"
            message_TXT += row["day"] + '-' + row["date"]
            message_TXT += "\n"
            # print "row:\n",row

            # Lunch:
            if (row["lunch_arr"]):
                message_TXT += "ناهار:"
                message_TXT += "\n"
            for lunch in row["lunch_arr"]:

                # message_TXT += "------------------\n"
                if(lunch["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (lunch["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (lunch["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (lunch["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += lunch["meal_name"]
                message_TXT += '\n'

            if (row["dinner_arr"] and row["lunch_arr"]):
                message_TXT += "*****\n"
            # Dinner:
            if(row["dinner_arr"]):
                message_TXT += "شام:"
                message_TXT += "\n"
            for dinner in row["dinner_arr"]:

                # message_TXT += "------------------\n"
                if (dinner["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (dinner["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (dinner["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (dinner["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += dinner["meal_name"]
                message_TXT += '\n'

        return message_TXT
    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_data")
        return


def next_week_data(userID):
    try:
        selected_PLCs = get_selected_PLCs(userID)

        if(len(selected_PLCs)>1):#It's not empty
            tmp_PLCs = users_PLCs[userID]
            PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            for elem in selected_PLCs:
                PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="NEXT_WEEK_"+ elem))

            bot.send_message(userID, MSGs.select_PLC,reply_markup = PLCs_markup)
        elif (len(selected_PLCs) == 1):
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'nextweek')
            if check == "OK":
                response = extract_DINING_next_weeks_data(userID,
                                                          selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'nextweek')
        else:
            bot.send_message(userID, MSGs.no_selected_PLCs)

    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.next_week_data")
        return
def extract_DINING_next_weeks_data(userID,PLCnum):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter_next_week)
            temp_data = scriptCaller.get_user_next_week_DINING_data(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID,
                                                          PLCnum)
            print str(temp_data)
            if (temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID, MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if (temp_data["PASSWORD_STATE"] == "WRONG"):
            return MSGs.your_password_is_wrong

        message_TXT = ""
        message_TXT += "موجودی: \n" + str('%.3f' % temp_data["Balance"]) + '\n'
        if(float(temp_data["Balance"]) < -10):
            message_TXT += emojize("❗اعتبارت کمه، یکم بیشترش کن❗️")
        bot.send_message(userID, message_TXT)

        message_TXT = ""
        bot.send_message(userID, "هفته بعد:")
        for row in temp_data["COMPLETE_TABLE"]:
            message_TXT += "==================\n"
            message_TXT += row["day"] + '-' + row["date"]
            message_TXT += "\n"
            # print "row:\n",row

            # Lunch:
            if (row["lunch_arr"]):
                message_TXT += "ناهار:"
                message_TXT += "\n"
            for lunch in row["lunch_arr"]:

                # message_TXT += "------------------\n"
                if(lunch["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (lunch["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (lunch["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (lunch["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += lunch["meal_name"]
                message_TXT += '\n'

            if (row["dinner_arr"] and row["lunch_arr"]):
                message_TXT += "*****\n"
            # Dinner:
            if(row["dinner_arr"]):
                message_TXT += "شام:"
                message_TXT += "\n"
            for dinner in row["dinner_arr"]:

                # message_TXT += "------------------\n"
                if (dinner["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (dinner["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (dinner["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (dinner["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += dinner["meal_name"]
                message_TXT += '\n'

        bot.send_message(userID,message_TXT)
        return None
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_next_weeks_data")
        return


def extract_DINING_places(userID):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_get_places)
            temp_data = scriptCaller.get_places_to_reserve_DINING(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID)
            print temp_data
            if(temp_data == None):
                bot.send_message(userID,MSGs.we_cant_do_it_now)
                return
            if (temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID, MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if (temp_data["PASSWORD_STATE"] == "WRONG"):
            bot.send_message(userID, MSGs.your_password_is_wrong, reply_markup=MSGs.enter_userpass_markup)
            return
        else:
            dataBase.update_UserPass(userID, users_book[userID]["user"], users_book[userID]["pass"])

        #Success!!! we have the data now, we can process it:
        temp_PLC = temp_data["Place"] # temp_PLC is now a dictionary "<number>":"<Place name>"
        temp_selected_PLCs = get_selected_PLCs(userID)

        #Saving to the memory and database
        dataBase.update_PLC_database(userID,temp_PLC,temp_selected_PLCs)
        users_PLCs[userID] = temp_PLC
        users_selected_PLCs[userID] = temp_selected_PLCs

        PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
        for elem in sorted(temp_PLC.keys()):
            if elem in temp_selected_PLCs:
                emoji_check = '✅'
            else:
                emoji_check = '❌'
            PLCs_markup.add(types.InlineKeyboardButton(emojize(emoji_check + temp_PLC[elem]), callback_data= "PLC_" + elem))
        PLCs_markup.add(types.InlineKeyboardButton("تموم", callback_data="PLC_DONE"))
        bot.send_message(userID,"لیست مکان‌هایی که می‌توان رزرو را انجام داد(پس از پایان انتخاب گزینه تموم را انتخاب کنید):",reply_markup=PLCs_markup)
        return
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_places")
        return
def get_selected_PLCs(userID):
    if userID not in users_selected_PLCs.keys():
        users_selected_PLCs[userID] = []
    return users_selected_PLCs[userID]


def STARTorder_meal(userID):
    try:
        selected_PLCs = get_selected_PLCs(userID)

        if(len(selected_PLCs)>1):#It's not empty
            tmp_PLCs = users_PLCs[userID]
            PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            for elem in selected_PLCs:
                PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="ORDER_NEXT_WEEK_"+ elem))

            bot.send_message(userID, MSGs.select_PLC,reply_markup = PLCs_markup)
        elif (len(selected_PLCs) == 1):
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'ordermeal')
            if check == "OK":
                response = order_meal_next_week(userID,
                                               selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'ordermeal')
        else:
            bot.send_message(userID, MSGs.no_selected_PLCs)

    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.STARTorder_meal")
        return
def order_meal_next_week(userID,PLCnum):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user_next_week_DINING_data(users_book[userID]["user"],
                                                                    users_book[userID]["pass"],
                                                                    userID,
                                                                    PLCnum)
            print temp_data
            if (temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID, MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if (temp_data["PASSWORD_STATE"] == "WRONG"):
            return MSGs.your_password_is_wrong

        if(float(temp_data["Balance"]) < -15):
            tmp_MSG = "حاجییییییی(یا خانم محترم)، اوضاع اعتبار حسابت خیلی خرابه:"
            tmp_MSG += '\n'
            tmp_MSG += "میزان اعتبار:"
            tmp_MSG += '\n'
            tmp_MSG += str(temp_data["Balance"])
            bot.send_message(userID,tmp_MSG)
            tmp_MSG = "ممکن هست در فرآیند سفارش بعضی از وعده‌ها گرفته نشه."
            bot.send_message(userID, tmp_MSG)

        user_meal_menu[userID] = temp_data["COMPLETE_TABLE"]
        users_book[userID]["state"] = 0
        user_order_list[userID]={}
        user_order_list[userID]["PLCnum"] = PLCnum
        ask_to_choose_meal(userID)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.order_meal_next_week")
        return
def ask_to_choose_meal(userID):
    try:
        Markup = types.InlineKeyboardMarkup(row_width=1)
        message_TXT = ""

        while users_book[userID]["state"] < 14:# 7 days a week for lunch and 7 days for dinner (starts from 0)
            message_TXT = "انتخاب کنید:\n"
            focused_row = users_book[userID]["state"] % 7

            message_TXT += user_meal_menu[userID][focused_row]["day"]
            message_TXT += "\n"
            message_TXT += user_meal_menu[userID][focused_row]["date"]

            if users_book[userID]["state"] < 7:
                message_TXT += "\n"
                message_TXT += "وعده ناهار:"
                something_to_order = False
                for idx,elem in enumerate(user_meal_menu[userID][focused_row]["lunch_arr"]):
                    if(elem["status"] == "AWAITING"):
                        Markup.add(types.InlineKeyboardButton(
                            elem["meal_name"],
                            callback_data=str(idx)))
                        something_to_order = True

                if(something_to_order):
                    Markup.add(types.InlineKeyboardButton(
                        "نمی‌خوام",
                        callback_data="nevermind"))
                    break
                else:
                    users_book[userID]["state"] = users_book[userID]["state"] + 1
                    continue
            elif users_book[userID]["state"] < 14:
                message_TXT += "\n"
                message_TXT += "وعده شام:"
                something_to_order = False
                for idx, elem in enumerate(user_meal_menu[userID][focused_row]["dinner_arr"]):# TODO replace all the meal_arrs with dinner_arr or lunch_arr
                    if (elem["status"] == "AWAITING"):
                        Markup.add(types.InlineKeyboardButton(
                            elem["meal_name"],
                            callback_data=str(idx)))
                        something_to_order = True

                if (something_to_order):
                    Markup.add(types.InlineKeyboardButton(
                        "نمی‌خوام",
                        callback_data="nevermind"))
                    break
                else:
                    users_book[userID]["state"] = users_book[userID]["state"] + 1
                    continue

        if(users_book[userID]["state"] == 14):# process the request here
            users_book[userID]["state"] = None
            bot.send_message(userID, "در حال ثبت درخواست...")
            # processing the request:
            print user_order_list[userID]
            print "----submitting----"
            submit_next_weeks_DINING_order(userID)
        else:
            bot.send_message(userID,message_TXT,reply_markup = Markup)
            users_book[userID]["state"] = users_book[userID]["state"] + 1
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.ask_to_choose_meal")
        return
def submit_next_weeks_DINING_order(userID):
    try:
        PLCnum = user_order_list[userID]["PLCnum"]
        del user_order_list[userID]["PLCnum"]
        # first check if there is anything to submit:
        submit = False
        for elem in user_order_list[userID].values():
            if(elem != "nevermind"):
                submit = True
                break

        if(not submit):
            bot.send_message(userID,MSGs.there_is_nothing_to_submit)
            extract_DINING_next_weeks_data(userID,PLCnum)
            return

        tempdata = scriptCaller.order_next_week_DINING_meal(users_book[userID]["user"],
                                                 users_book[userID]["pass"],
                                                 userID,
                                                 user_order_list[userID],
                                                 PLCnum)
        extract_DINING_next_weeks_data(userID,PLCnum)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.submit_next_weeks_DINING_order")
        return


def wait_for_feedback(userID):
    try:
        users_book[userID]["state"] = "FeedBack"
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.wait_for_feedback")
        return

def STARTget_priority(userID):
    try:
        selected_PLCs = get_selected_PLCs(userID)

        if(len(selected_PLCs)>1):#It's not empty
            tmp_PLCs = users_PLCs[userID]

            # PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
            # for elem in selected_PLCs:
            #     PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="PRI_"+ elem))
            #
            # bot.send_message(userID, "محلی که وعده ناهار را دریافت می‌کنید، انتخاب کنید:",reply_markup = PLCs_markup)

            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'get_pri')
            if check == "OK":
                response = extract_DINING_priority(userID,
                                                          selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'get_pri')

        elif (len(selected_PLCs) == 1):
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'get_pri')
            if check == "OK":
                response = extract_DINING_priority(userID,
                                                          selected_PLCs[0])
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'get_pri')
        else:
            bot.send_message(userID, MSGs.no_selected_PLCs)

    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.STARTget_priority")
        return
def extract_DINING_priority(userID,PLCnum):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user__DINING_priority_list(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID,
                                                          PLCnum)
            print str(temp_data)
            if (temp_data["ENTRY_STATE"] == "BAD"):
                bot.send_message(userID, MSGs.trying_again)
                attempts = attempts + 1
                continue
            else:
                break
        if (temp_data["ENTRY_STATE"] == "BAD"):
            return MSGs.cant_do_it_now

        if (temp_data["PASSWORD_STATE"] == "WRONG"):
            return MSGs.your_password_is_wrong

        message_TXT = ""
        print ":::;;;:::"
        print temp_data["Meal_Points"]
        sorted_data = sorted(temp_data["Meal_Points"].items(), key=operator.itemgetter(1),reverse=True)
        for idx,elem in enumerate(sorted_data):
            message_TXT += str(idx) + '. ' + elem[0] + ': ' + str(elem[1])
            message_TXT += '\n'

        bot.send_message(userID,message_TXT)
        return None
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_priority")
        return


