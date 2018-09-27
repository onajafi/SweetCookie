#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from telebot import types

none_markup = types.InlineKeyboardMarkup(row_width=1)

enter_userpass_markup = types.InlineKeyboardMarkup(row_width=1)
enter_userpass_markup.add(types.InlineKeyboardButton('ورود اطلاعات کاربری',callback_data='UserPass'))

get_forgotten_code = types.InlineKeyboardMarkup(row_width=1)
get_forgotten_code.add(types.InlineKeyboardButton('گرفتن کد فراموشی',callback_data='FCode'))

reserve_time_markup = types.InlineKeyboardMarkup(row_width=1)
reserve_time_markup.add(types.InlineKeyboardButton('رزرو هفته بعد',callback_data='OrderNextWeek'))

greetings = """سلام،
این بات برای سهولت رزرو از سایت dining.sharif.edu ساخته شده است.
با وارد کردن اطلاعات کاربری، شما با <a href="https://github.com/onajafi/SweetCookie/blob/Develop/termsAndConditions/temsAndCons.md/">شرایط و قوانین</a> استفاده از این بات موافقت کرده‌اید."""

give_user = "نام کاربری را وارد کنید" \
            "(نام کاربری پیش‌فرض شماره دانشجویی می‌باشد):"

give_pass = "رمز را وارد کنید" \
            "(گذرواژه پیش‌فرض کد ملی می‌باشد):"

your_password_is_wrong = """رمز یا نام کاربری اشتباه می‌باشد.
مجددا اطلاعات کاربری را وارد کنید."""

trying_to_enter= "در حال ورود...(2min)"

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


