#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback
from inits import bot

f = open('../error.txt', 'w+')
f.close()

def log_error(title):
    try:
        f = open('../error.txt', 'a')
        f.write("\n\n\n" + str(title) + "-------------------\n")
        traceback.print_exc(file=f)
        f.close()
    except:
        print "Error in log() error handler :/"


# This is a function decorator to keep it from killing the hole bot when giving an error
# def secure(FUNC):
#     try:
#
#     except:
#         bot.send_message(userID,MSGs.we_cant_do_it_now)
#         log_error("ERROR: users.this_week_data")
#         return


