from .base import tg_id, user_id, to_json, is_reply, is_admin
from .beyonder import datetime_arg, duration, seq, time_mode, drink_seq, optional_time_mode
from .wiki import ga_name, seq_name, path_name, group_name, is_all, value
from .organ import organ_id, organ_value, rank, organ_mode, titul, titul_mode, organ_name
from .newspaper import news_paper_id, optional_news_paper_id, news_paper_mode, news_paper_value, news_paper_name

class Optionals:
    tg_id = tg_id
    user_id = user_id
    to_json = to_json
    seq = seq
    drink_seq = drink_seq
    time_mode = optional_time_mode
    ga_name = ga_name
    seq_name = seq_name
    path_name = path_name
    group_name = group_name
    is_all = is_all
    is_reply = is_reply
    value = value
    is_admin = is_admin
    rank = rank
    titul = titul
    organ_id = organ_id
    organ_value = organ_value
    organ_name = organ_name
    news_paper_id = news_paper_id
    optional_news_paper_id = optional_news_paper_id
    news_paper_name = news_paper_name
    news_paper_value = news_paper_value
    user_id = user_id

class Requireds:
    date = datetime_arg
    duration = duration
    time_mode = time_mode
    organ_mode = organ_mode
    titul_mode = titul_mode
    news_paper_mode = news_paper_mode
    news_paper_name = news_paper_name
    news_paper_id = news_paper_id
