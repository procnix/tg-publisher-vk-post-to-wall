import datetime as DT
from db.db_interval import get_time_interval

cache_interval = {}
cache_timestamp = {}

def convert_time(user_id):
    t1 = DT.datetime.now()
    if user_id not in cache_interval:
        cache_interval[user_id] = get_time_interval(user_id)
    if user_id not in cache_timestamp:
        cache_timestamp[user_id] = t1
    t2 = cache_timestamp[user_id] + DT.timedelta(hours=int(cache_interval[user_id]))
    if t2 - cache_timestamp[user_id] >= DT.timedelta(days=1):
        t2 = t2.replace(hour=0, minute=0, second=0) + DT.timedelta(days=1)
        cache_timestamp[user_id] = t2
    cache_timestamp[user_id] = t2
    return t2.replace(microsecond=0).timestamp()
