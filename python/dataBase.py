#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import ast
import sqlite3
from datetime import datetime


def get_users_book_from_database():
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        DB_table = cur.fetchall()
        print DB_table
        output_users = {}
        for elem in DB_table:
            output_users[elem[0]] = {"user": elem[5], "pass":elem[6], "state": None}
        return output_users

def check_STR(input):
    if input is None:
        return '-'
    return input

def _add_user(message):
    with sqlite3.connect("../users.sqlite") as conn:
        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?,?);",
                           (message.from_user.id,
                            check_STR(message.from_user.username),
                            check_STR(message.from_user.first_name),
                            check_STR(message.from_user.last_name),
                            datetime.now(),
                            None,
                            None))

def check_the_user_in_DB(message):
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE u_id=?",(message.from_user.id,))
        sample_test = cur.fetchone()
        if sample_test is not None:
            return True
        _add_user(message)
        return False

def update_UserPass(userID,username_DINING,password_DINING):
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET diningUSR=?, diningPASS=? WHERE u_id=?",
                    (username_DINING,password_DINING,userID))
        conn.commit()

#Places:
def _add_PLC(userID, PLCs_Dictionary, selected_PLCs = []):
    with sqlite3.connect("../users.sqlite") as conn:
        conn.execute("INSERT INTO places VALUES (?, ?, ?);",
                           (userID,
                            str(PLCs_Dictionary),
                            str(selected_PLCs)))

#update or add the places the user can reserve
def update_PLC_database(userID,PLCs_Dictionary,selected_PLCs = []):
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM places WHERE u_id=?",(userID,))
        sample_test = cur.fetchone()
        if sample_test == None:# we have a new place list
            conn.execute("INSERT INTO places VALUES (?, ?, ?);",
                         (userID,
                          str(PLCs_Dictionary),
                          str(selected_PLCs)))
            return False
        else:# update the existing place list of the user
            conn.execute("UPDATE places SET PLCs=?,selected_PLCs=? WHERE u_id=?",
                         (str(PLCs_Dictionary),
                          str(selected_PLCs),
                          userID))
            return True

def get_users_PLCs_from_database():
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM places")
        DB_table = cur.fetchall()
        print DB_table
        output_users = {}
        for elem in DB_table:
            output_users[elem[0]] = ast.literal_eval(elem[1])
        return output_users

def get_users_selected_PLCs():
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM places")
        DB_table = cur.fetchall()
        print DB_table
        output_users = {}
        for elem in DB_table:
            output_users[elem[0]] = ast.literal_eval(elem[2])
        return output_users

# Priorities:
# Write to DB
def update_PRI_LIST_database(userID,pri_list,sel_days = []):
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM auto_res_data WHERE u_id=?",(userID,))
        sample_test = cur.fetchone()
        if sample_test == None:# we have a new priority list
            conn.execute("INSERT INTO auto_res_data VALUES (?, ?, ?);",
                         (userID,
                          str(pri_list),
                          str(sel_days)))
            return False
        else:# update the existing priority list of the user
            conn.execute("UPDATE auto_res_data SET pri_arr=?,selected_days=? WHERE u_id=?",
                         (str(pri_list),
                          str(sel_days),
                          userID))
            return True


# Read from DB:
def get_users_PRI_LIST():
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM auto_res_data")
        DB_table = cur.fetchall()
        print DB_table
        output_pri_list = {}
        for elem in DB_table:
            output_pri_list[elem[0]] = ast.literal_eval(elem[1])
        return output_pri_list

def get_users_AUTO_RES_DAYS():
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM auto_res_data")
        DB_table = cur.fetchall()
        print DB_table
        selected_dates_to_res = {}
        for elem in DB_table:
            selected_dates_to_res[elem[0]] = ast.literal_eval(elem[2])
        return selected_dates_to_res

#Delete in DB:
def delete_user_AUTO_RES_DATA(userID):
    with sqlite3.connect("../users.sqlite") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM auto_res_data WHERE u_id=?",(userID,))

with sqlite3.connect("../users.sqlite") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "u_id MEDIUMINT, "
                "u_name VARCHAR(100), "
                "u_first_name VARCHAR(100), "
                "u_last_name VARCHAR(100), "
                "u_time DATETIME, "
                "diningUSR VARCHAR(100),"
                "diningPASS VARCHAR(100));")
    cur.execute("CREATE TABLE IF NOT EXISTS places("
                "u_id MEDIUMINT, "
                "PLCs TEXT, "
                "selected_PLCs TEXT);")
    cur.execute("CREATE TABLE IF NOT EXISTS auto_res_data("
                "u_id MEDIUMINT, "
                "pri_arr TEXT,"
                "selected_days TEXT);")

    conn.commit()






