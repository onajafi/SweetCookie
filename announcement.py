#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Send a message to all users:

from inits import bot
import dataBase
import sqlite3
import traceback

# Enter the message here:
MSG = "بات آپدیت شد(V0.4):"

with sqlite3.connect("users.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    DB_table = cur.fetchall()
    print DB_table
    for elem in DB_table:
        try:
            bot.send_message(elem[0],MSG)
        except:
            print '--------'
            traceback.print_exc()






