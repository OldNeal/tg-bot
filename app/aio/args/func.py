from datetime import datetime, timedelta
import re
from app.exception.args import DataFormatError, DurationFormatError, DrinkPathNameError, SeqError

def is_datetime(s):
    """Проверяет наличие даты в разных форматах"""
    formats = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d-%m-%Y',
        '%Y.%m.%d',
    ]
    for fmt in formats:
        try:
            return bool(datetime.strptime(s, fmt))
        except ValueError:
            continue
    
    raise DataFormatError(f"Значение не является датой")

def parse_date(s):
    """Парсит дату в разных форматах"""
    formats = [
        '%Y-%m-%d',
        '%d.%m.%Y',
        '%d-%m-%Y',
        '%Y.%m.%d',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    
    raise DataFormatError(f"Значение не является датой")

def is_time_pattern(arg):
    """
    Проверяет, является ли аргумент временной меткой.
    Поддерживает: +2d5h, -7m, +1s, -2h, +30m, -1d, +2d5h30m
    """
    # Паттерн: знак (+ или -), затем цифры и буквы (d, h, m, s)
    # Допускает комбинации: 2d5h, 30m, 1s, 2d, 5h30m и т.д.
    pattern = r'^[\+-]?\d+[ydhms](?:\d+[ydhms])*$'
    if re.match(pattern, arg):
        return True
    raise DurationFormatError(f"Значение не является временным промежутком")

def parse_duration(s):
    """
    Парсит длительность вида:
    - 5h      -> -5h (отрицательное, знак по умолчанию -)
    - +5h     -> +5h (положительное)
    - 2d5h    -> -2d -5h (отрицательное)
    - +2d5h   -> +2d +5h (положительное)
    - -5h     -> -5h (явное отрицательное)
    """
    
    # Проверяем формат: сначала опциональный знак, затем части с единицами
    pattern = r'^([+-])?((?:\d+[ydhmws])+)$'
    match = re.match(pattern, s)
    
    if not match:
        raise DurationFormatError(f"Значение не является временным промежутком")
    
    operator = match.group(1)  # Может быть None, '+', или '-'
    units_part = match.group(2)
    
    # Если знак не указан, по умолчанию '-'
    if operator is None:
        operator = '-'
    
    # Парсим каждую часть: 1h, 30m, 2d и т.д.
    unit_pattern = r'(\d+)([ydhms])'
    total = timedelta()
    
    for value_str, unit in re.findall(unit_pattern, units_part):
        value = int(value_str)
        
        # Применяем знак к каждой части
        if operator == '-':
            value = -value
        # Если '+', оставляем как есть
        
        if unit == 's':
            total += timedelta(seconds=value)
        elif unit == 'm':
            total += timedelta(minutes=value)
        elif unit == 'h':
            total += timedelta(hours=value)
        elif unit == 'd':
            total += timedelta(days=value)
        elif unit == 'y':
            total += timedelta(days=value * 365)
        elif unit == 'w':
            total += timedelta(days=value * 7)
    
    return total

def check_path_name(path: str | None):
    if path is None:
        raise DrinkPathNameError('Не указал путь нужного зелья')
    return bool(path)

def check_seq(seq: int):
    if not(10 > seq > -2):
        raise SeqError('Указал несуществующую последовательность')
    return seq