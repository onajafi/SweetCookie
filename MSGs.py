#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from telebot import types

none_markup = types.InlineKeyboardMarkup(row_width=1)

enter_userpass_markup = types.InlineKeyboardMarkup(row_width=1)
enter_userpass_markup.add(types.InlineKeyboardButton('ورود اطلاعات کاربری',callback_data='UserPass'))

get_forgotten_code = types.InlineKeyboardMarkup(row_width=1)
get_forgotten_code.add(types.InlineKeyboardButton('گرفتن کد فراموشی',callback_data='FCode'))

greetings = """سلام،
این بات برای سهولت رزرو از سایت dining.sharif.edu ساخته شده است.
با وارد کردن اطلاعات کاربری، شما با <a href="http://www.example.com/">شرایط و قوانین</a> استفاده از این بات موافقت کرده‌اید."""

give_user = "نام کاربری را وارد کنید" \
            "(نام کاربری پیش‌فرض شماره دانشجویی می‌باشد):"

give_pass = "رمز را وارد کنید" \
            "(گذرواژه پیش‌فرض کد ملی می‌باشد):"

your_password_is_wrong = """رمز یا نام کاربری اشتباه می‌باشد.
مجددا اطلاعات کاربری را وارد کنید."""

trying_to_enter= "در حال ورود...(2min)"

trying_to_enter_next_week= "در حال دریافت برنامه هفته بعد...(2min)"

trying_to_get_the_menu= "در حال دریافت لیست...(2min)"

there_is_nothing_to_submit = "غذایی ثبت نشده..."

trying_again = "مشکل در بالا آوردن سایت، تلاش مجدد...(2min)"

we_cant_do_it_now = "در حال حاضر، انجام عملیات امکان پذیر نمی‌باشد."

cant_do_it_now = "سایت یه مشکلی داره، بعد از چند دقیقه دوباره امتحان کن"

please_enter_your_UserPass = "قبل از هر کاری اطلاعات ورودت رو بده"
