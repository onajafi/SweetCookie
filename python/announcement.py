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
بات آپدیت شد :)
آپدیت ۰.۷:
- درست شدن مشکل دریافت کد برای وعده‌های شام و سلف های دیگر.(مرسی امیر ضیایی)
- اضافه شدن نام وعده غذا در هنگام دریافت کد فراموشی.
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






