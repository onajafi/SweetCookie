#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from telebot import types
from emoji import emojize
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

none_markup = types.InlineKeyboardMarkup(row_width=1)

enter_userpass_markup = types.InlineKeyboardMarkup(row_width=1)
enter_userpass_markup.add(types.InlineKeyboardButton('ورود اطلاعات کاربری',callback_data='UserPass'))

get_forgotten_code = types.InlineKeyboardMarkup(row_width=1)
get_forgotten_code.add(types.InlineKeyboardButton('دریافت کد فراموشی',callback_data='FCode'))

reserve_time_markup = types.InlineKeyboardMarkup(row_width=1)
reserve_time_markup.add(types.InlineKeyboardButton('رزرو هفته بعد',callback_data='OrderNextWeek'))

simple_MAIN_markup = types.ReplyKeyboardMarkup()
simple_BTN_res = types.KeyboardButton(emojize('رزرو هفته بعد:telephone:', use_aliases=True))
simple_BTN_Show_This_week = types.KeyboardButton(emojize('نمایش هفته جاری:chart_with_downwards_trend:', use_aliases=True))
simple_BTN_FCode = types.KeyboardButton(emojize('دریافت کد فراموشی:u6307:', use_aliases=True))
simple_BTN_ADV = types.KeyboardButton(emojize('لیست دستورات:ledger:', use_aliases=True))
simple_MAIN_markup.row(simple_BTN_res,simple_BTN_Show_This_week)
simple_MAIN_markup.row(simple_BTN_FCode,simple_BTN_ADV)

greetings = """سلام،
این بات برای سهولت رزرو از سایت dining.sharif.edu ساخته شده است.
با وارد کردن اطلاعات کاربری، شما با <a href="https://github.com/onajafi/SweetCookie/blob/Develop/termsAndConditions/temsAndCons.md/">شرایط و قوانین</a> استفاده از این بات موافقت کرده‌اید."""

give_user = "نام کاربری را وارد کنید" \
            "(نام کاربری پیش‌فرض شماره دانشجویی می‌باشد):"

give_pass = "رمز را وارد کنید" \
            "(گذرواژه پیش‌فرض کد ملی می‌باشد):"

your_password_is_wrong = """رمز یا نام کاربری اشتباه می‌باشد.
مجددا اطلاعات کاربری را وارد کنید."""

trying_to_enter= "در حال اتصال به وبگاه...(2min)"

trying_to_enter_next_week= "در حال دریافت برنامه هفته بعد...(2min)"

trying_to_get_the_menu= "در حال دریافت لیست...(2min)"

trying_to_get_places= "در حال دریافت مکان‌های تحویل وعده...(1min)"

there_is_nothing_to_submit = "غذایی ثبت نشده..."

trying_again = "مشکل در بالا آوردن سایت، تلاش مجدد...(2min)"

we_cant_do_it_now = "در حال حاضر، انجام عملیات امکان پذیر نمی‌باشد."

in_the_middle_of_a_process = "بات در حال پردازش دستور قبل است.\n حداکثر تا چند دقیقه دیگر آزاد می‌شود."

Stop_Spamming = "اسپم نکن..."

cant_do_it_now = "سایت یه مشکلی داره، بعد از چند دقیقه دوباره امتحان کن"

please_enter_your_UserPass = "قبل از هر کاری اطلاعات ورودت رو بده"

its_reserve_time = "وقت رزرو شده..."

give_your_feedback = "پیامتان را بفرستید:"

feedBack_sent = "پیامتان ارسال شد :)"

no_selected_PLCs = "هنوز جایی برای تحویل وعده غذایی مشخص نکردید:\n از دستور /set_places استفاده کنید."

select_PLC = "محل را انتخاب کنید:"

how_to_use = """لیست کامل دستورات:
/ordermeal - رزرو هفته بعد

/nextweek - نمایش برنامه غذایی هفته بعد

/thisweek - نمایش برنامه غذایی هفته جاری

/fcode - دریافت کد فراموشی

/feedback - ارسال نظر

/set_places - انتخاب محل(های) دریافت وعده غذایی
"""
lets_start = "انتخاب کنید"

How_much_credit = "میزان افزایش اعتبار(به تومان) را وارد کنید(حداقل ۱۰۰):"

didnt_get_the_credit_inc_amount = "متاسفانه میزان افزایش اعتبار دریافت نشد، دوباره امتحان کنید"

payment_warning = emojize( """نکات زیر را حتما بخوانید:
:exclamation:
وظیفه این بات سهولت استفاده از امکانات رزرو است و سازندگان بات قصد گرفتن اطلاعات بانکی یا دریافت پول از شما را ندارند. بدین منظور با انتخاب دکمه پرداخت، شما به درگاه پرداخت دانشگاه شریف اتصال پیدا می‌کنید که کاملا از کنترل ربات خارج است.
:exclamation:
بعد از تایید شدن پرداخت، شما وارد صفحه‌ای می‌شوید که از شما درخواست می‌شود اطلاعات حساب خود را وارد کنید(اگر وارد نکنید اعتبار شما افزایش پیدا نمی‌کند و ممکن است از حساب کارت شما کم شود!)."""
,use_aliases=True)
