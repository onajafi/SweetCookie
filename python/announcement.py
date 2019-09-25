#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Send a message to all users:

from inits import bot,feedBack_target_chat
import dataBase
import sqlite3
import traceback
import MSGs

# Enter the message here:
MSG = """سلام،
یک سال از شروع فعالیت این ربات اینترنتی، Sweet Cookie، می‌گذره.
از اینکه این بات رو با کم و کسری هاش استفاده کردین از شما ممنونم.
اگر فارغ التحصیل شدین یا تمایل به استفاده از این ربات رو ندارین میتونین با زدن دستور
/restart 
اطلاعات رمز و نام کاربریتون رو از سیستم حذف کنین.

در ضمن وقت رزرو شده، رزرو یادتون نره:
/ordermeal 
"""

with sqlite3.connect("../users.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    DB_table = cur.fetchall()
    print DB_table
    success = 0
    crashes = 0
    for elem in DB_table:
        try:
            bot.send_message(elem[0],MSG,reply_markup = MSGs.simple_MAIN_markup)
            success = success + 1
        except:
            print '--------'
            crashes = crashes + 1
            # traceback.print_exc()
            try:# Added this to make sure every thing is running as smooth as possible
                bot.send_message(feedBack_target_chat,"This guy blocked the bot:\n" +
                                 str(elem[2]) + "\n" +
                                 str(elem[3]) + "\n" +
                                 str(elem[0])) #remove this markup after the first announcement
            except:
                pass

    bot.send_message(feedBack_target_chat,"Finished the announcement\nPassed: " +
                     str(success)+
                     "\nFailed: "+
                     str(crashes))






