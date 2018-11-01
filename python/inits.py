# This file contains the classified settings of the bot...
#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import telebot

tel_token = "<###THE BOTS TOKEN###>" #TEST token

feedBack_target_chat = <---CHAT_ID---> #The chat where all the FeedBacks will be forwarded, Make sure the bot has access to this chat

bot = telebot.TeleBot(tel_token)
