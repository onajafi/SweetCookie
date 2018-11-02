#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback
from inits import bot
import MSGs

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
# The Function (FUNC) has only 1 argument which is the userID
def secure_from_exception(FUNC):
    def output_FUNC(input_userID):
        try:
            FUNC(input_userID)
        except:
            bot.send_message(input_userID,MSGs.we_cant_do_it_now)
            log_error("ERROR: " + FUNC.__name__)
            return
    return output_FUNC

