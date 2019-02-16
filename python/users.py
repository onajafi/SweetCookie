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
users_pri_list = dataBase.get_users_PRI_LIST() # maps to a list
users_auto_res_days = dataBase.get_users_AUTO_RES_DAYS() # maps to a list
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
call_PRIORITY_pattern = re.compile("^PRI_[0-9]{1,2}$")
call_AUTO_RES_pattern = re.compile("^AUTO_RES_[A-Z]{1,2}$")
call_AUTO_RES_DAY_SEL_pattern = re.compile("^AUTO_RES_DAY_SEL_[0-9]{1,2}$")
message_number = re.compile("^[0-9]*$")

serve_times_in_a_week = { 1: "شنبه - ناهار",
                        2: "یک‌شنبه - ناهار",
                        3: "دوشنبه - ناهار",
                        4: "سه‌شنبه - ناهار",
                        5: "چهارشنبه - ناهار",
                        6: "پنج‌شنبه - ناهار",
                        7: "جمعه - ناهار",

                        8: "شنبه - شام",
                        9: "یک‌شنبه - شام",
                        10: "دوشنبه - شام",
                        11: "سه‌شنبه - شام",
                        12: "چهارشنبه - شام",
                        13: "پنج‌شنبه - شام",
                        14: "جمعه - شام",
                       }

def FA_UNI_to_EN_DIGIT_CONV(FAnumber):
    ENnumber = ""
    # uniFAnum = unicode(FAnumber, "utf-32")
    for dig in FAnumber:
        try:
            ENnumber = ENnumber + str(int(dig))
        except:
            pass
    return ENnumber

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
        elif (users_book[userID]["state"] == "AUTO_RES_A"):  # In this state the user is able to change the priority list
            pass # TODO do we have to do something with this? or should we stick with the user friendly plan?
        elif(users_book[userID]["state"] == "getIncCreditAmount"):
            users_book[userID]["state"] = None
            number_val = FA_UNI_to_EN_DIGIT_CONV(message_TXT)
            if(message_number.match(number_val) and len(number_val) > 2):
                check = trafficController.check_spam(userID, 'COMM_inc_credit')
                if check == "OK":
                    response = increase_DINING_credit(userID,number_val)
                    if response is not None:
                        bot.send_message(userID, response)
                    trafficController.finished_process(userID, 'COMM_inc_credit')
            else:
                bot.send_message(userID,MSGs.didnt_get_the_credit_inc_amount)
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

        elif(call_PRIORITY_pattern.match(call_TXT)):
            PLC_number = re.search('[0-9]{1,2}', call_TXT).group(0)

            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'get_pri')
            if check == "OK":
                response = extract_DINING_priority(userID,
                                                   PLC_number)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'get_pri')

            users_book[userID]["state"] = "AUTO_RES_A"
        elif(users_book[userID]["state"] == "AUTO_RES_A" and call_TXT == 'AUTO_RES_A'):# TODO Here we have to save the current list in the database

            bot.edit_message_reply_markup(userID, ACT_call.message.message_id, reply_markup=MSGs.none_markup)

            DEFAULT_SERVE_TIMES = [1,2,3,4]
            # dataBase.update_PRI_LIST_database(userID,users_pri_list[userID],DEFAULT_SERVE_TIMES)
            users_auto_res_days[userID] = DEFAULT_SERVE_TIMES


            TEMP_SERVE = users_auto_res_days[userID]
            SERVE_markup = types.InlineKeyboardMarkup(row_width=2)
            for lunch,dinner in zip([1,2,3,4,5,6,7],[8,9,10,11,12,13,14]):
                if lunch in TEMP_SERVE:
                    lunch_emoji_check = '✅'
                else:
                    lunch_emoji_check = '❌'

                if dinner in TEMP_SERVE:
                    dinner_emoji_check = '✅'
                else:
                    dinner_emoji_check = '❌'

                SERVE_markup.add(types.InlineKeyboardButton(emojize(dinner_emoji_check + serve_times_in_a_week[dinner]),
                                               callback_data="AUTO_RES_DAY_SEL_" + str(dinner)),
                    types.InlineKeyboardButton(emojize(lunch_emoji_check + serve_times_in_a_week[lunch]),
                                               callback_data="AUTO_RES_DAY_SEL_" + str(lunch))
                )
            SERVE_markup.add(types.InlineKeyboardButton("ثبت", callback_data="AUTO_RES_DAY_SEL_DONE"))

            bot.send_message(userID,"برای چه وعده‌هایی می‌خواهید رزرو خودکار انجام شود؟\nپس از انتخاب دکمه ثبت را بزنید",
                             reply_markup=SERVE_markup)
            users_book[userID]["state"] = "AUTO_RES_SEL_DAYS"

        elif(users_book[userID]["state"] == "AUTO_RES_SEL_DAYS" and call_AUTO_RES_DAY_SEL_pattern.match(call_TXT)):
            SERVE_number = int(re.search('[0-9]{1,2}', call_TXT).group(0))

            print SERVE_number
            print users_auto_res_days[userID]
            print SERVE_number in users_auto_res_days[userID]
            if (SERVE_number in users_auto_res_days[userID]):  # the user wants to cancel this days meal
                users_auto_res_days[userID].remove(SERVE_number)
                # print "REMOVED"
            else:
                users_auto_res_days[userID].append(SERVE_number)

            print users_auto_res_days[userID]

            TEMP_SERVE = users_auto_res_days[userID]
            SERVE_markup = types.InlineKeyboardMarkup(row_width=2)
            for lunch, dinner in zip([1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14]):
                if lunch in TEMP_SERVE:
                    lunch_emoji_check = '✅'
                else:
                    lunch_emoji_check = '❌'

                if dinner in TEMP_SERVE:
                    dinner_emoji_check = '✅'
                else:
                    dinner_emoji_check = '❌'

                SERVE_markup.add(types.InlineKeyboardButton(emojize(dinner_emoji_check + serve_times_in_a_week[dinner]),
                                                            callback_data="AUTO_RES_DAY_SEL_" + str(dinner)),
                                 types.InlineKeyboardButton(emojize(lunch_emoji_check + serve_times_in_a_week[lunch]),
                                                            callback_data="AUTO_RES_DAY_SEL_" + str(lunch))
                                 )
            SERVE_markup.add(types.InlineKeyboardButton("ثبت", callback_data="AUTO_RES_DAY_SEL_DONE"))

            bot.edit_message_reply_markup(userID, ACT_call.message.message_id, reply_markup=SERVE_markup)

        elif (users_book[userID]["state"] == "AUTO_RES_SEL_DAYS" and call_TXT == "AUTO_RES_DAY_SEL_DONE"):
            print "users_pri_list",users_pri_list
            print "users_auto_res_days", users_auto_res_days
            dataBase.update_PRI_LIST_database(userID, users_pri_list[userID], users_auto_res_days[userID])

            temp_SERVE_DAYS = users_auto_res_days[userID]

            if (temp_SERVE_DAYS):  # If it's not NULL
                temp_MSG = "وعده‌هایی که برای رزرو خودکار انتخاب شدن:"
                temp_MSG += '\n'
                for elem in sorted(temp_SERVE_DAYS):
                    temp_MSG += emojize('✅' + serve_times_in_a_week[elem])
                    temp_MSG += '\n'
            else:
                temp_MSG = "هیچ وعده‌ای انتخاب نشده :("

            bot.edit_message_text(temp_MSG, userID, ACT_call.message.message_id, reply_markup=MSGs.none_markup)

            temp_PLC = users_PLCs[userID]
            temp_selected_PLCs = users_selected_PLCs[userID]
            if (temp_selected_PLCs):  # If it's not NULL
                MSG_sel_PLCs = "در این مکان‌(ها) رزرو خودکار انجام می‌شود:"
                MSG_sel_PLCs += '\n'
                for elem in sorted(temp_PLC.keys()):
                    if elem in temp_selected_PLCs:
                        MSG_sel_PLCs += emojize('✅' + temp_PLC[elem])
                        MSG_sel_PLCs += '\n'
            else:
                MSG_sel_PLCs = "هنوز جایی برای رزرو وعده انتخاب نشده... :(\nاز دستور /set_places استفاده کنید.\n"

            bot.send_message(userID, MSGs.auto_res_is_setup_PARTA + MSG_sel_PLCs + MSGs.auto_res_is_setup_PARTC, reply_markup=MSGs.simple_MAIN_markup)

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
            meal_type = "dinner"
        else:
            meal_type = "lunch"

        attempts = 1
        while attempts <= 3:
            if(meal_type == "dinner"):
                bot.send_message(userID,"در حال دریافت کد فراموشی وعده شام")
            elif(meal_type == "lunch"):
                bot.send_message(userID, "در حال دریافت کد فراموشی وعده ناهار")

            temp_data = scriptCaller.get_user_DINING_forgotten_code(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID,
                                                          PLCnum,
                                                          meal_type)
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

        bot.send_message(userID,temp_data["alert_info"])
        if(temp_data["LIMIT_IS_REACHED"] == "TRUE"):
            bot.send_message(userID,"تمومش کردی که؟!؟!\nتا آخر ترم باید با کارت دانشجویی، غذات رو تحویل بگیری...")
            return

        if(temp_data["MEAL_IS_AVAILABLE"] == "FALSE"):
            bot.send_message(userID,"ظاهرا برای این وعده رزروی انجام نشده :(")
            return

        if("FCode" not in temp_data.keys()):
            bot.send_message(userID, MSGs.we_cant_do_it_now)
            return


        message_TXT = ""
        message_TXT += "کد فراموشی: \n" + str(temp_data["FCode"])
        message_TXT += "\n"
        message_TXT += str(temp_data["meal_name"])

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
            bot.send_message(userID,"در حال دریافت برنامه هفته جاری")
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

        bot.send_message(userID,message_TXT)
        return None
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

@Error_Handle.secure_from_exception
def STARTincreasing_credit(userID):
    users_book[userID]["state"] = "getIncCreditAmount"
    bot.send_message(userID,MSGs.How_much_credit)
def increase_DINING_credit(userID,amount):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, "در حال انتقال درخواست پرداخت")
            temp_data = scriptCaller.get_user_DINING_inc_credit_link(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID,
                                                          amount)
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

        message_TXT = "با انتخاب دکمه زیر وارد درگاه پرداخت دانشگاه شریف می‌شوید:"
        message_TXT += '\n'
        message_TXT += "میزان افزایش اعتبار: "
        message_TXT += amount
        message_TXT += " تومان"

        print temp_data["URL"]

        payBTN = types.InlineKeyboardMarkup(row_width=1)
        payBTN.add(types.InlineKeyboardButton('ورود به درگاه پرداخت', url=temp_data["URL"]))

        bot.send_message(userID,MSGs.payment_warning)
        bot.send_message(userID,message_TXT,reply_markup=payBTN)
        return None
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.increase_DINING_credit")
        return

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


# def STARTget_priority(userID):
#     try:
#         selected_PLCs = get_selected_PLCs(userID)
#
#         if(len(selected_PLCs)>1):#It's not empty #TODO think about this part...
#             tmp_PLCs = users_PLCs[userID]
#
#             # PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
#             # for elem in selected_PLCs:
#             #     PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="PRI_"+ elem))
#             #
#             # bot.send_message(userID, "محلی که وعده ناهار را دریافت می‌کنید، انتخاب کنید:",reply_markup = PLCs_markup)
#
#             trafficController.drop_check(userID)
#             check = trafficController.check_spam(userID, 'get_pri')
#             if check == "OK":
#                 response = extract_DINING_priority(userID,
#                                                           selected_PLCs[0])
#                 if response is not None:
#                     bot.send_message(userID, response)
#                 trafficController.finished_process(userID, 'get_pri')
#
#         elif (len(selected_PLCs) == 1):
#             trafficController.drop_check(userID)
#             check = trafficController.check_spam(userID, 'get_pri')
#             if check == "OK":
#                 response = extract_DINING_priority(userID,
#                                                           selected_PLCs[0])
#                 if response is not None:
#                     bot.send_message(userID, response)
#                 trafficController.finished_process(userID, 'get_pri')
#
#         else:
#             bot.send_message(userID, MSGs.no_selected_PLCs)
#
#     except:
#         bot.send_message(userID,MSGs.we_cant_do_it_now)
#         Error_Handle.log_error("ERROR: users.STARTget_priority")
#         return
def extract_DINING_priority(userID,PLCnum):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, "در حال استخراج برنامه‌ی غذایی هفته‌های قبل")
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
            message_TXT += str(idx + 1) + '. ' + elem[0] + ': ' + str(elem[1])
            message_TXT += '\n'

        temp_user_markup = types.InlineKeyboardMarkup(row_width=1)
        temp_user_markup.add(types.InlineKeyboardButton('مرحله بعد',callback_data='AUTO_RES_A'))

        bot.send_message(userID,"لیست اولویت‌های غذایی شما:\n" + message_TXT,reply_markup=temp_user_markup)
        dataBase.update_PRI_LIST_database(userID,sorted_data)
        users_pri_list[userID] = sorted_data
        return None
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_priority")
        return
@Error_Handle.secure_from_exception
def STARTset_auto_res(userID):# TODO test this with a proper account
    selected_PLCs = get_selected_PLCs(userID)

    if (len(selected_PLCs) > 1):  # It's not empty
        tmp_PLCs = users_PLCs[userID]

        PLCs_markup = types.InlineKeyboardMarkup(row_width=1)
        for elem in selected_PLCs:
            PLCs_markup.add(types.InlineKeyboardButton(tmp_PLCs[elem], callback_data="PRI_"+ elem))

        bot.send_message(userID, "محلی را که بیشترین تعداد وعده ناهار را دریافت می‌کنید، انتخاب کنید:",reply_markup = PLCs_markup)
    elif (len(selected_PLCs) == 1):
        trafficController.drop_check(userID)
        check = trafficController.check_spam(userID, 'get_pri')
        if check == "OK":
            response = extract_DINING_priority(userID,
                                               selected_PLCs[0])
            if response is not None:
                bot.send_message(userID, response)
            trafficController.finished_process(userID, 'get_pri')

        users_book[userID]["state"] = "AUTO_RES_A"
    else:
        bot.send_message(userID, MSGs.no_selected_PLCs)


@Error_Handle.secure_from_exception
def START_comm_to_test_auto_res(userID):# This is for testing the reserve
    if (userID not in users_auto_res_days.keys()):
        bot.send_message(userID,MSGs.please_setup_the_auto_res)
        return None

    selected_PLCs = get_selected_PLCs(userID)

    if (len(selected_PLCs) > 1):  # It's not empty #TODO test this (it's going to reserve in all the places)

        for elem in selected_PLCs:
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'auto_res')
            if check == "OK":
                bot.send_message(userID, "در حال انجام رزرو خودکار...")
                response = do_DINING_auto_reserve(userID, elem)
                if response is not None:
                    bot.send_message(userID, response)
                trafficController.finished_process(userID, 'auto_res')

    elif (len(selected_PLCs) == 1):
        trafficController.drop_check(userID)
        check = trafficController.check_spam(userID, 'auto_res')
        if check == "OK":
            bot.send_message(userID, "در حال انجام رزرو خودکار...")
            response = do_DINING_auto_reserve(userID,
                                               selected_PLCs[0])
            if response is not None:
                bot.send_message(userID, response)
            trafficController.finished_process(userID, 'auto_res')
    else:
        bot.send_message(userID, MSGs.no_selected_PLCs)

# returns an error message in str, otherwise it will return a True, showing every is fine
@Error_Handle.secure_from_exception
def START_auto_res_quiet(userID):
    selected_PLCs = get_selected_PLCs(userID)

    if (len(selected_PLCs) > 1):  # It's not empty #TODO test this (it's going to reserve in all the places)

        for elem in selected_PLCs:
            trafficController.drop_check(userID)
            check = trafficController.check_spam(userID, 'auto_res')
            if check == "OK":
                response = do_DINING_auto_reserve(userID, elem)
                if response is not None:
                    bot.send_message(userID, "خطا در انجام رزرو خودکار:\n" + response)
                trafficController.finished_process(userID, 'auto_res')

    elif (len(selected_PLCs) == 1):
        trafficController.drop_check(userID)
        check = trafficController.check_spam(userID, 'auto_res')
        if check == "OK":
            response = do_DINING_auto_reserve(userID,
                                               selected_PLCs[0])
            if response is not None:
                    bot.send_message(userID, "خطا در انجام رزرو خودکار:\n" + response)
            trafficController.finished_process(userID, 'auto_res')
    else:
        bot.send_message(userID, "خطا در انجام رزرو خودکار:\n" + MSGs.no_selected_PLCs)

@Error_Handle.secure_from_exception_2input
def do_DINING_auto_reserve(userID,PLCnum):
    # if(users_pri_list[userID] == None): #TODO complete this if you need it
    #     bot.send_message(userID,)

    #Turn the pri_list into a dictionary:
    input_list = users_pri_list[userID]
    pri_dict = {}
    for elem in input_list:
        pri_dict[elem[0]] = elem[1]

    attempts = 1
    while attempts <= 3:
        # bot.send_message(userID, "در حال رزرو خودکار...")
        temp_data = scriptCaller.auto_res_DINING_by_pri_list(users_book[userID]["user"],
                                                            users_book[userID]["pass"],
                                                            userID,
                                                            PLCnum,
                                                            pri_dict,
                                                            users_auto_res_days[userID])#TODO add this to the function input
        print str(temp_data)
        if (temp_data["ENTRY_STATE"] == "BAD"):
            # bot.send_message(userID, MSGs.trying_again)
            attempts = attempts + 1
            continue
        elif(temp_data["ORDERED_MEALS_STAT"] == False):# Better do this quietly
            print "attempting again..."
            attempts = attempts + 1
            continue
        else:
            break
    if (temp_data["ENTRY_STATE"] == "BAD"):
        return MSGs.cant_do_it_now

    if (temp_data["PASSWORD_STATE"] == "WRONG"):
        return MSGs.your_password_is_wrong

    if(temp_data["Balance"] < -20.000):
        return "میزان اعتبار شما از حداقل مجاز کمتر است" + '\n' + temp_data["Balance"]
    else:
        bot.send_message(userID,"رزرو خودکار با موفقیت انجام شد :)")
    extract_DINING_next_weeks_data(userID,PLCnum)
    return None


@Error_Handle.secure_from_exception
def test(userID):
    message = ""
    for elem in users_pri_list[userID]:
        message += elem[0] + '\n'

    bot.send_message(userID,message)





