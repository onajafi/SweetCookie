import datetime

def get_time():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3,minutes=30)

def IsDinnerTime():
    now = get_time()
    dinner_time_start = now.replace(hour=15, minute=0, second=0, microsecond=0)
    dinner_time_end = now.replace(hour=23, minute=0, second=0, microsecond=0)
    if(dinner_time_start < now and now < dinner_time_end):
        return True

def IsLunchTime():
    now = get_time()
    lunch_time_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    lunch_time_end = now.replace(hour=15, minute=0, second=0, microsecond=0)
    if(lunch_time_start < now and now < lunch_time_end):
        return True

def giveServeNumber():
    now = get_time()
    return ((now.weekday() + 2) % 7) + 1
