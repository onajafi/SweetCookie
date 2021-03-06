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

cancel_auto_res_markup = types.InlineKeyboardMarkup(row_width=1)
cancel_auto_res_markup.add(types.InlineKeyboardButton('لغو رزرو خودکار',callback_data='CancelAutoRes'))

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

give_your_feedback = "پیامتان را ارسال کنید:\n" \
                     "(برای لغو از دستور /cancel استفاده کنید)"

feedBack_sent = "پیامتان ارسال شد :)"

no_selected_PLCs = "هنوز جایی برای تحویل وعده غذایی مشخص نکردید:\n از دستور /set_places استفاده کنید."

select_PLC = "محل را انتخاب کنید:"

how_to_use = """لیست کامل دستورات:
/ordermeal - رزرو هفته بعد
----------------------------------------
/nextweek - نمایش برنامه غذایی هفته بعد

/thisweek - نمایش برنامه غذایی هفته جاری
----------------------------------------
/fcode - دریافت کد فراموشی
----------------------------------------
/feedback - ارسال نظر
----------------------------------------
/set_places - انتخاب محل(های) دریافت وعده غذایی
----------------------------------------
/set_auto_res - تنظیم رزرو خودکار

/test_auto_res - تست رزرو خودکار

/cancel_auto_res - لغو رزرو خودکار
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

auto_res_is_setup_PARTA = "رزرو خودکار برای شما فعال شد\nهر سه شنبه بعد از ظهر، بات برای شما رزرو را انجام می‌دهد\n"

auto_res_is_setup_PARTC = "با وارد کردن دستور /test_auto_res می‌توانید عملیات رزرو خودکار را تست کنید." \
                          "برای لغو رزرو خودکار از دستور /cancel_auto_res استفاده کنید."

please_setup_the_auto_res = "ابتدا باید تنظیمات رزرو خودکار را انجام دهید\n دستور زیر را وارد کنید:\n" \
                            "/set_auto_res"

out_of_range_row_num = "شماره ردیف پیدا نشد :("

how_to_set_priotrities = """برای تغییر لیست بالا ابتدا شماره ردیف غذا و سپس امتیاز مربوط را بصورت زیر وارد کنید:
<MEAL_ROW_NUMBER> <SCORE>
برای مثال برای بازنویسی امتیاز غذای موجود در ردیف ۲۳ به مقدار ۴۰ عبارت زیر را وارد کنید:
23 40

در غیر این صورت دکمه مرحله بعد را انتخاب کنید.
‌"""

are_you_sure_cancel_auto_res = "آیا مطمئنید که می‌خواهید رزرو خودکار را لغو کنید؟\n" \
                               "با انجام این کار تمام اطلاعت مربوط به رزرو خودکار (اولویت‌ها و وعده‌های انتخاب شده)پاک خواهد شد."

auto_res_cancelled = "رزرو خودکار با موفقیت لغو شد.\n" \
                     "از این به بعد بات هر سه شنبه بعد از ظهر یک پیام یادآوری رزرو ارسال خواهد کرد.\n" \
                     "‌"

you_dont_have_auto_res = "رزرو خودکاری برای این کاربر تعریف نشده :))"

canceled_successfully = "عملیات کنسل شد"



