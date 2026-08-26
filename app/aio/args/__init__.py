from .base import tg_id, to_json, is_reply, is_admin, is_delay
from .beyonder import datetime_arg, duration, seq, time_mode, drink_seq, optional_time_mode
from .wiki import ga_name, seq_name, path_name, group_name, is_all, value
from .organ import organ_id, organ_value, rank, organ_mode, titul, titul_mode, organ_name

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
    is_delay = is_delay
    rank = rank
    organ_id = organ_id
    titul = titul

class Requireds:
    date = datetime_arg
    duration = duration
    time_mode = time_mode
    organ_value = organ_value
    organ_mode = organ_mode
    titul_mode = titul_mode
    organ_name = organ_name

base_args = [Optionals.tg_id, Optionals.to_json, Optionals.is_reply, Optionals.is_admin, Optionals.is_delay]
