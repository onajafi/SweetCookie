#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback

f = open('error.txt', 'w+')
f.close()

def log_error(title):
    try:
        f = open('error.txt', 'a')
        f.write("\n\n\n" + str(title) + "-------------------\n")
        traceback.print_exc(file=f)
        f.close()
    except:
        print "Error in log() error handler :/"






