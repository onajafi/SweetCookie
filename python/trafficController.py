#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from datetime import datetime
from inits import bot
import MSGs

# Dictionary format-> userID:(type,time)
last_user_msg = {}

long_process = {"fcode",'CALL','ordermeal','thisweek','nextweek','fcode',
                'CALL_UserPass','CALL_FCode','CALL_OrderNextWeek',"SCRIPT",
                'set_places','get_pri','COMM_inc_credit'}

short_process = {'start','text','COMM_nextweek','COMM_thisweek','COMM_fcode',
                 'COMM_ordermeal','COMM_get_pri','COMM_help','inc_credit'}


#This function will check if a user is
# using the proper amount of load on the server
## returns "SPAM" if it's a spam (not implemented)
## "IGNORE" if there is no need to take any action
## "IN_PROC" tell that where in a process right now
## "OK" if everything is cool
def check_spam(userID,MSG_type):
    if userID in last_user_msg.keys():
        print last_user_msg[userID]
        if last_user_msg[userID][0] in long_process:
            if (datetime.now() - last_user_msg[userID][1]).total_seconds() < 130:
                bot.send_message(userID,
                                 MSGs.in_the_middle_of_a_process)
                return "IN_PROC"
        elif last_user_msg[userID][0] in short_process:
            if (datetime.now() - last_user_msg[userID][1]).total_seconds() < 0.5:
                bot.send_message(userID,
                                 MSGs.Stop_Spamming)
                return "IGNORE"
        else:
            print "--IGNORING--"
            return "IGNORE"

    last_user_msg[userID] = (MSG_type,
                             datetime.now())
    return "OK"

def finished_process(userID,MSG_type):
    if userID in last_user_msg.keys() and last_user_msg[userID][0]==MSG_type:
        del last_user_msg[userID]
        print "++PROCESS FINISHED++"

def drop_check(userID):
    if userID in last_user_msg.keys():
        del last_user_msg[userID]



