#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Send a message to all users:

from inits import bot,feedBack_target_chat
import dataBase
import sqlite3
import traceback

# Enter the message here:
MSG = """سلام،
خیلی ممنون از اینکه این بات رو امتحان کردین.
از زمانی که این بات ریلیز شد دقیقا ۳۰ نفر بات رو /start کردن و از بین این تعداد ۱۳ نفر امکانات مختلف این بات رو استفاده کردن.

سعی کردم این بات رو باتوجه به فیدبکی که از شما داشتم آپدیت کنم.
آپدیت ۰.۵:
- برطرف شدن مشکل رزرو کاربران خوابگاهی (مرسی از کمکت میلاد جلالی و علی عسگری!)
- امکان انتخاب مکان رزرو از طریق دستور /set_places
- برطرف شدن باگ reminder

در آپدیت بعدی بات، امکان رزرو خودکار اضافه می‌شه و بعد از تست‌های نهایی بات رو بطور کامل ریلیز می‌کنیم!
اگر باگی پیدا کردین از طریق دستور /feedback برام ارسال کنید.

با تشکر
امید نجفی
:D

"""

with sqlite3.connect("users.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    DB_table = cur.fetchall()
    print DB_table
    success = 0
    crashes = 0
    for elem in DB_table:
        try:
            bot.send_message(elem[0],MSG)
            success = success + 1
        except:
            print '--------'
            crashes = crashes + 1
            traceback.print_exc()
            try:# Added this to make sure every thing is running as smooth as possible
                bot.send_message(feedBack_target_chat,"This guy made the bot crash:\n" + str(elem[0]))
            except:
                pass

    bot.send_message(feedBack_target_chat,"Finished the announcement\nPassed: " +
                     str(success)+
                     "\nFailed: "+
                     str(crashes))






