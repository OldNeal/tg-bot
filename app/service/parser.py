import argparse, shlex, re
from datetime import timedelta, datetime, time

def parse_user(s: str):
        if s.startswith('id') and s.removeprefix('id').isdigit():
            return int(s.removeprefix('id'))
        elif s.startswith('@'):
            return s.removeprefix('@')
        elif s.isdigit():
            return int(s)
        else:
            return s


def parse_date(s):
    """Парсит дату/время в разных форматах"""
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
    
    raise argparse.ArgumentTypeError(f"Неверный формат даты: {s}")

def parse_duration(s):
    """Парсит длительность вида: 1h30m, 2d, 5m, 10s"""
    
    # Регулярное выражение для разбора
    pattern = r'^(\d+)([ydhms])$'
    match = re.match(pattern, s)
    
    if not match:
        raise argparse.ArgumentTypeError(f"Неверный формат длительности: {s}")
    
    value = int(match.group(1))
    unit = match.group(2)
    
    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    elif unit == 'y':
        return timedelta(days=value*365)

class BotCommand:
    argparse = argparse

    def __init__(self, cmd: str):
        self.cmd = cmd
        default_config_parsers = {'add_help':False, 'exit_on_error':False}

        self.wiki = self.argparse.ArgumentParser(**default_config_parsers)
        self.wiki.add_argument('value', nargs='?')
        self.wiki.add_argument('-n', '--name')
        self.wiki.add_argument('-id', type=int)
        self.wiki.add_argument('--all', action='store_true', dest='is_all')

        self.seq_redact = self.argparse.ArgumentParser(**default_config_parsers)
        self.seq_redact.add_argument('-s', '--seq', type=int)
        self.seq_redact.add_argument('-p', '--path')
        
        self.beyonder = self.argparse.ArgumentParser(**default_config_parsers)
        self.beyonder.add_argument('user', type=parse_user, nargs='?')
        self.beyonder.add_argument('-id', type=int, dest='user_id')
        self.beyonder.add_argument('-u', '--username', '--user-name', type=str, dest='user_name')
        self.beyonder.add_argument('-r', '--reply', action='store_true', dest='is_reply')
        self.beyonder.add_argument('-a', '--admin', action='store_true', dest='is_admin')

        beyonder_parents = default_config_parsers | {'parents':[self.beyonder]}
        seq_redact_parents = default_config_parsers | {'parents':[self.beyonder, self.seq_redact]}
        wiki_parents = default_config_parsers | {'parents':[self.wiki]}

        self.parser = self.argparse.ArgumentParser(**default_config_parsers)
        self.subparsers = self.parser.add_subparsers(dest='command')
    
        self.info = self.subparsers.add_parser('/info', **beyonder_parents)
    
        self.drink = self.subparsers.add_parser('/drink', **seq_redact_parents)

        self.upseq = self.subparsers.add_parser('/upseq', **seq_redact_parents)

        self.downseq = self.subparsers.add_parser('/downseq', **seq_redact_parents)

        self.kill = self.subparsers.add_parser('/kill', **beyonder_parents)

        self.time = self.subparsers.add_parser('/time', argument_default='info', **default_config_parsers)
        self.time_subparsers = self.time.add_subparsers(dest='mode', required=False)

        self.time_redact= self.time_subparsers.add_parser('info', **beyonder_parents)

        self.time_redact= self.time_subparsers.add_parser('redact', **beyonder_parents)
        self.time_redact.add_argument('operator', choices=['-', '+'])
        self.time_redact.add_argument('duration', type=parse_duration)
        self.time_redact.add_argument('-y', '--years', type=lambda x: timedelta(days=int(x)*365))
        self.time_redact.add_argument('--months', type=lambda x: timedelta(days=int(x)*30))
        self.time_redact.add_argument('-d', '--days', type=lambda x: timedelta(days=int(x)))
        self.time_redact.add_argument('-h', '--hours', type=lambda x: timedelta(hours=int(x)))
        self.time_redact.add_argument('-m', '--minutes', type=lambda x: timedelta(minutes=int(x)))
        self.time_redact.add_argument('-s', '--seconds', type=lambda x: timedelta(seconds=int(x)))

        self.time_replace = self.time_subparsers.add_parser('replace', **beyonder_parents)
        self.time_replace.add_argument('date', type=parse_date)
        
        self.path = self.subparsers.add_parser('/path', **wiki_parents)
        self.ga = self.subparsers.add_parser('/ga', **wiki_parents)
        self.seq = self.subparsers.add_parser('/seq', **wiki_parents)
        self.group = self.subparsers.add_parser('/group', **default_config_parsers)
        self.group.add_argument('name')
    

    def split(self, args: str):
        return shlex.split(args)
    
    @property
    def args(self):
        return self.parser.parse_args(self.split(self.cmd))

commands_examples = [
    # === /info - информация о пользователе ===
    "/info",  # о себе
    "/info 123456",  # по ID
    "/info id123456",  # по ID с префиксом
    "/info @JohnDoe",  # по юзернейму
    "/info JohnDoe",  # по имени
    "/info -id 123456",  # через флаг
    "/info -u JohnDoe",  # через флаг username
    "/info -r",  # с ответом
    "/info -a",  # как админ
    "/info 123456 -r -a",  # комбинированный
    
    # === /drink - выпить ===
    "/drink",  # для себя
    "/drink 123456",
    "/drink @JohnDoe",
    "/drink -id 123456",
    "/drink -u JohnDoe",
    "/drink -s 5",  # последовательность
    "/drink -p /path/to/file",  # путь
    "/drink -s 5 -p /path/to/file",  # для себя с параметрами
    "/drink 123456 -s 5 -p /path/to/file",
    "/drink @JohnDoe -s 5 -p /path/to/file",
    
    # === /upseq - поднять последовательность ===
    "/upseq",  # для себя
    "/upseq 123456",
    "/upseq @JohnDoe",
    "/upseq -id 123456",
    "/upseq -u JohnDoe",
    "/upseq -s 10",
    "/upseq -p /path/to/file",
    "/upseq 123456 -s 10 -p /path/to/file",
    "/upseq @JohnDoe -s 10 -p /path/to/file",
    
    # === /downseq - опустить последовательность ===
    "/downseq",  # для себя
    "/downseq 123456",
    "/downseq @JohnDoe",
    "/downseq -id 123456",
    "/downseq -u JohnDoe",
    "/downseq -s 3",
    "/downseq -p /path/to/file",
    "/downseq 123456 -s 3 -p /path/to/file",
    "/downseq @JohnDoe -s 3 -p /path/to/file",
    
    # === /kill - кик/бан ===
    "/kill 123456",
    "/kill @JohnDoe",
    "/kill -id 123456",
    "/kill -u JohnDoe",
    "/kill 123456 -r",  # с ответом
    "/kill 123456 -a",  # как админ
    "/kill 123456 -r -a",
    
    # === /time info - информация о времени ===
    "/time info",  # свое время
    "/time info 123456",
    "/time info @JohnDoe",
    "/time info -id 123456",
    "/time info -u JohnDoe",
    "/time info 123456 -r",  # с ответом
    "/time info 123456 -a",  # как админ
    
    # === /time redact - редактирование времени ===
    "/time redact 123456 + 2h",
    "/time redact 123456 - 30m",
    "/time redact @JohnDoe + 1d",
    "/time redact -id 123456 - 5m",
    "/time redact -u JohnDoe + 2h",
    "/time redact + 2h",  # для себя
    
    # С дополнительными опциями
    "/time redact 123456 + 2h -y 1",  # +2 часа и +1 год
    "/time redact 123456 + 2h --months 3",  # +2 часа и +3 месяца
    "/time redact 123456 + 2h -d 1",  # +2 часа и +1 день
    "/time redact 123456 + 2h -h 3",  # +2 часа и +3 часа (всего 5 часов)
    "/time redact 123456 + 2h -m 30",  # +2 часа 30 минут
    "/time redact 123456 + 2h -s 15",  # +2 часа 15 секунд
    
    # Комбинированные
    "/time redact 123456 + 1y -d 5 -h 2 -m 30 -s 10",
    "/time redact @JohnDoe - 30m -d 1 -h 1",
    
    # === /time replace - замена времени ===
    "/time replace 123456 2026-06-19",
    "/time replace 123456 19.06.2026",
    "/time replace 123456 19-06-2026",
    "/time replace 123456 2026.06.19",
    "/time replace @JohnDoe 2026-06-19",
    "/time replace -id 123456 2026-06-19",
    "/time replace -u JohnDoe 2026-06-19",
    "/time replace 2026-06-19",  # для себя
    
    # === /path - работа с путями ===
    "/path",
    "/path /new/path",
    "/path -n PathName",
    "/path -id 123",
    "/path --all",
    "/path /new/path -n PathName --all",
    
    # === /ga - работа с GA ===
    "/ga",
    "/ga 100",
    "/ga -n GAName",
    "/ga -id 123",
    "/ga --all",
    "/ga 100 -n GAName --all",
    
    # === /seq - работа с последовательностями ===
    "/seq",
    "/seq 42",
    "/seq -n SeqName",
    "/seq -id 123",
    "/seq --all",
    "/seq 42 -n SeqName --all",
    
    # === /group - работа с группами ===
    "/group mygroup",
    "/group admins",
    "/group moderators",

    # Числовой ID
    "/info 123456",
    "/time redact 123456 + 2h",
    "/kill 123456 -r",
    
    # ID с префиксом 'id'
    "/info id123456",
    "/time redact id123456 + 2h",
    "/kill id123456 -r",
    
    # Юзернейм с @
    "/info @JohnDoe",
    "/time redact @JohnDoe + 2h",
    "/kill @JohnDoe -r",
    
    # Обычное имя
    "/info JohnDoe",
    "/time redact JohnDoe + 2h",
    "/kill JohnDoe -r",
    
    # Через флаги
    "/info -id 123456",
    "/time redact -id 123456 + 2h",
    "/info -u JohnDoe",
    "/time redact -u JohnDoe + 2h",

    "/time redact 123456 + 10s",   # 10 секунд
    "/time redact 123456 + 5m",    # 5 минут
    "/time redact 123456 + 2h",    # 2 часа
    "/time redact 123456 + 3d",    # 3 дня
    "/time redact 123456 + 1y",    # 1 год

    "/time replace 123456 2026-06-19",   # YYYY-MM-DD
    "/time replace 123456 19.06.2026",   # DD.MM.YYYY
    "/time replace 123456 19-06-2026",   # DD-MM-YYYY
    "/time replace 123456 2026.06.19",   # YYYY.MM.DD
]

if __name__ == '__main__':
    [print(s, BotCommand(s).args) for s in commands_examples]

