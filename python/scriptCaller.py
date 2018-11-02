#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, subprocess, signal
import time
import json

import Error_Handle

if not os.path.exists('../tmp'):
    os.makedirs('../tmp')

webCrawlingScriptFolder = '../casperJS/'

def get_user_DINING_data(username,password,chat_id,PLCnum):
    input_data = {"pass":password,"user":username,"chat_id":chat_id,"PLCnum":PLCnum}
    input_file_name = 'input_EXT_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'extract_data.js',input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_user_DINING_data")
        print "Script KILLED"
        return

    if(p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_EXT_'+ str(chat_id) + '.json'
    #--Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def get_user_next_week_DINING_data(username,password,chat_id,PLCnum):
    input_data = {"pass":password,"user":username,"chat_id":chat_id,"PLCnum":PLCnum}
    input_file_name = 'input_EXT_W2_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'extract_next_weeks_data.js',input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_user_next_week_DINING_data")
        print "Script KILLED"
        return

    if(p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_EXT_W2_'+ str(chat_id) + '.json'
    #--Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def get_user_DINING_forgotten_code(username,password,chat_id,PLCnum,meal_type):
    input_data = {"pass": password,
                  "user": username,
                  "chat_id": chat_id,
                  "PLCnum":PLCnum,
                  "meal_type":meal_type}
    input_file_name = 'input_GFC_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)
    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'get_forgotten.js',input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_user_DINING_forgotten_code")
        print "Script KILLED"
        return

    if(p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_GFC_'+ str(chat_id) + '.json'
    #--Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def order_next_week_DINING_meal(username,password,chat_id,order_list,PLCnum):

    input_data = {"pass": password,
                  "user": username,
                  "chat_id": chat_id,
                  "order_list":order_list,
                  "PLCnum":PLCnum}

    input_file_name = 'input_RES_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'resMeal.js',input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: order_next_week_DINING_meal")
        print "Script KILLED"
        return

    if(p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_RES_'+ str(chat_id) + '.json'
    #--Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def get_places_to_reserve_DINING(username,password,chat_id):
    input_data = {"pass": password,
                  "user": username,
                  "chat_id": chat_id}

    input_file_name = 'input_PLC_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'get_Places.js',input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_places_to_reserve_DINING")
        print "Script KILLED"
        return

    if(p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_PLC_'+ str(chat_id) + '.json'
    #--Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def get_user__DINING_priority_list(username,password,chat_id,PLCnum):

    input_data = {"pass": password,
                  "user": username,
                  "chat_id": chat_id,
                  "PLCnum": PLCnum}

    input_file_name = 'input_PRI_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'extract_priorities.js', input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_user__DINING_priority_list")
        print "Script KILLED"
        return

    if (p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_PRI_' + str(chat_id) + '.json'
    # --Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data

def get_user_DINING_inc_credit_link(username,password,chat_id,amount):

    input_data = {"pass": password,
                  "user": username,
                  "chat_id": chat_id,
                  "amount": amount}

    input_file_name = 'input_INC_' + str(chat_id) + '.json'
    with open('../tmp/' + input_file_name, 'w') as outfile:
        json.dump(input_data, outfile)

    try:
        p = subprocess.Popen(['casperjs',webCrawlingScriptFolder + 'increase_credit.js', input_file_name])
        print p.poll()
        for i in range(120):
            if (p.poll() is None):
                time.sleep(1)
    except:
        p.send_signal(signal.SIGINT)
        Error_Handle.log_error("SCRIPT ERROR: get_user_DINING_inc_credit_link")
        print "Script KILLED"
        return

    if (p.poll() is None):
        p.send_signal(signal.SIGINT)
        print "CTRL+C The script didn't get completely finished"
        return
    print "--DONE--"

    data = None
    data_output_file_name = 'output_INC_' + str(chat_id) + '.json'
    # --Reading the results--
    with open('../tmp/' + data_output_file_name) as f:
        data = json.load(f)

    # os.remove('../tmp/' + data_output_file_name)
    # os.remove('../tmp/' + input_file_name)
    return data


