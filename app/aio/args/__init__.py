from .base import tg_id, to_json, is_reply, is_admin
from .beyonder import datetime_arg, duration, seq, time_mode, drink_seq, optional_time_mode
from .wiki import ga_name, seq_name, path_name, group_name, is_all, value

class Optionals:
    tg_id = tg_id
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

class Requireds:
    date = datetime_arg
    duration = duration
    time_mode = time_mode

base_args = [Optionals.tg_id, Optionals.to_json, Optionals.is_reply, Optionals.is_admin]
