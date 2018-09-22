#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import MSGs,scriptCaller
from inits import bot
from emoji import emojize
import dataBase
from telebot import types
import Error_Handle

import sys
reload(sys)
sys.setdefaultencoding('utf8')

users_book = dataBase.get_users_book_from_database()
user_meal_menu = {}
user_order_list = {}

def add_user(userID):
    try:
        if(userID not in users_book.keys()):
            users_book[userID] = {"user": None, "pass":None, "state":None}
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.add_user")
        return

def know_user(userID):
    try:
        if (userID not in users_book.keys()):
            return False
        return True
    except:
        Error_Handle.log_error("ERROR: users.know_user")
        return False

def process_user_MSG(userID, message_TXT):
    try:
        if(users_book[userID]["state"] == "GetUser"):
            users_book[userID]["user"] = message_TXT
            users_book[userID]["state"] = "GetPass"
            return MSGs.give_pass
        elif(users_book[userID]["state"] == "GetPass"):
            users_book[userID]["pass"] = message_TXT
            users_book[userID]["state"] = None
            return extract_DINING_data(userID)
        else:
            pass
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.process_user_MSG")
        return

def process_user_call(userID,call_TXT,ACT_call):
    try:
        if (call_TXT == "UserPass"):
            users_book[userID]["state"] = "GetUser"
            dataBase.update_UserPass(userID,None,None)
            return MSGs.give_user
        elif(call_TXT == "FCode"):#Forgotten Code
            if(users_book[userID]["user"] != None and users_book[userID]["pass"] != None):
                return scriptCaller.get_user_DINING_forgotten_code(users_book[userID]["user"],
                                                                   users_book[userID]["pass"],
                                                                   userID)
            else:
                bot.send_message(userID,MSGs.please_enter_your_UserPass,reply_markup=MSGs.enter_userpass_markup)
                return
        elif(users_book[userID]["state"] in (1,2,3,4,5,6,7) and
                     call_TXT in ("0","1","2","3","nevermind")):

            if(call_TXT == "nevermind"):
                appending_ans = "چیزی نمی‌خوام"
            else:
                appending_ans = user_meal_menu[userID][users_book[userID]["state"] - 1]["meal_arr"][int(call_TXT)]["meal_name"]

            bot.edit_message_text(text = ACT_call.message.text +"\n" + appending_ans,
                                  chat_id = userID,
                                  message_id = ACT_call.message.message_id,
                                  reply_markup = None)
            user_order_list[userID][users_book[userID]["state"] - 1] = call_TXT
            ask_to_choose_meal(userID)
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


def extract_DINING_data(userID):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID,MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user_DINING_data(users_book[userID]["user"],
                                              users_book[userID]["pass"],
                                              userID)
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
        message_TXT += "موجودی: \n" + str(temp_data["Balance"])
        bot.send_message(userID,message_TXT)

        message_TXT = ""
        bot.send_message(userID, "هفته جاری:")
        for row in temp_data["Table"]:
            message_TXT += "==================\n"
            message_TXT += row["day"] + '-' + row["date"]
            message_TXT += "\n"
            # print "row:\n",row
            for meal in row["meal_arr"]:

                message_TXT += "------------------\n"
                if(meal["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (meal["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (meal["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (meal["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += meal["meal_name"]
                message_TXT += '\n'
                # message_TXT += meal["status"]
        return message_TXT
    except:
        bot.send_message(userID,MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_data")
        return

def get_DINING_forgotten_code(userID):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user_DINING_forgotten_code(users_book[userID]["user"],
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

def extract_DINING_next_weeks_data(userID):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter_next_week)
            temp_data = scriptCaller.get_user_next_week_DINING_data(users_book[userID]["user"],
                                                          users_book[userID]["pass"],
                                                          userID)
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

        message_TXT = ""
        message_TXT += "موجودی: \n" + str(temp_data["Balance"])
        bot.send_message(userID, message_TXT)

        message_TXT = ""
        bot.send_message(userID, "هفته بعد:")
        for row in temp_data["Table"]:
            message_TXT += "==================\n"
            message_TXT += row["day"] + '-' + row["date"]
            message_TXT += "\n"
            # print "row:\n",row
            for meal in row["meal_arr"]:

                message_TXT += "------------------\n"
                if (meal["status"] == "OK_DONE"):
                    message_TXT += emojize("✅ ")
                elif (meal["status"] == "AWAITING"):
                    message_TXT += emojize("🛒 ")
                elif (meal["status"] == "OK_AWAITING"):
                    message_TXT += emojize("✅ ")
                elif (meal["status"] == "FAILED"):
                    message_TXT += emojize("❌ ")

                message_TXT += meal["meal_name"]
                message_TXT += '\n'
                # message_TXT += meal["status"]
        bot.send_message(userID,message_TXT)
        return None
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.extract_DINING_next_weeks_data")
        return

#TODO add the option where the credit value reaches the limit
def submit_next_weeks_DINING_order(userID):
    try:
        # first check if there is anything to submit:
        submit = False
        for elem in user_order_list[userID].values():
            if(elem != "nevermind"):
                True
                break

        if(not submit):
            bot.send_message(userID,MSGs.there_is_nothing_to_submit)
            extract_DINING_next_weeks_data(userID)
            return

        tempdata = scriptCaller.order_next_week_DINING_meal(users_book[userID]["user"],
                                                 users_book[userID]["pass"],
                                                 userID,
                                                 user_order_list[userID])
        extract_DINING_next_weeks_data(userID)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.submit_next_weeks_DINING_order")
        return

def ask_to_choose_meal(userID):
    try:
        Markup = types.InlineKeyboardMarkup(row_width=1)
        message_TXT = ""

        while users_book[userID]["state"] < 7:# 7 days a week (starts from 0)
            message_TXT = "انتخاب کنید:\n"
            focused_row = users_book[userID]["state"]

            message_TXT += user_meal_menu[userID][focused_row]["day"]
            message_TXT += "\n"
            message_TXT += user_meal_menu[userID][focused_row]["date"]

            something_to_order = False
            for idx,elem in enumerate(user_meal_menu[userID][focused_row]["meal_arr"]):
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

        if(users_book[userID]["state"] == 7):# TODO process the request here
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

def order_meal_next_week(userID):
    try:
        attempts = 1
        while attempts <= 3:
            bot.send_message(userID, MSGs.trying_to_enter)
            temp_data = scriptCaller.get_user_next_week_DINING_data(users_book[userID]["user"],
                                                                    users_book[userID]["pass"],
                                                                    userID)
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

        user_meal_menu[userID] = temp_data["Table"]
        users_book[userID]["state"] = 0
        user_order_list[userID]={}
        ask_to_choose_meal(userID)
    except:
        bot.send_message(userID, MSGs.we_cant_do_it_now)
        Error_Handle.log_error("ERROR: users.order_meal_next_week")
        return







