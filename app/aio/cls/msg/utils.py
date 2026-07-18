import random
import html
import json
import markdown
from typing import Any
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.text = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def get_data(self):
        return ''.join(self.text)

class TextHTMLBase(str):
    def blockquote(self, expandable: bool = False, cite: str | None = None) -> "TextHTML":
        """ Цитата
            - expandable: Позволяет сделать цитату разворачиваемой
            - cite: Автор цитаты"""
        return TextHTML(f'<blockquote {'expandable' if expandable else ''}>{self}{f'<cite>{cite}</cite>' if cite else ''}</blockquote>')

    def escape(self) -> "TextHTML":
        ''' Экранирование HTML '''
        return TextHTML(html.escape(self))
    
    def unescape(self) -> "TextHTML":
        ''' Обратное экранирование HTML '''
        return TextHTML(html.unescape(self))

    def bold(self) -> "TextHTML":
        ''' Жирный текст '''
        return TextHTML(f'<b>{self}</b>')

    def code(self) -> "TextHTML":
        ''' Моноширный (копируемый) текст '''
        return TextHTML(f'<code>{self}</code>')
    
    def italic(self) -> "TextHTML":
        ''' Курсивный текст '''
        return TextHTML(f'<i>{self}</i>')

    def href(self, url: str) -> "TextHTML":
        ''' Ссылка
            - url: Ссылка на ресурс '''
        return TextHTML(f'<a href="{url}">{self}</a>')
    
    def custom_emoji(self, emoji_id: str) -> "TextHTML":
        ''' Пользовательская эмодзи
            - emoji_id: ID пользовательской эмодзи '''
        return TextHTML(f'<tg-emoji emoji-id="{emoji_id}">{self}</tg-emoji>')
    
    def spoiler(self) -> "TextHTML":
        ''' Скрытый текст (спойлер) '''
        return TextHTML(f'<tg-spoiler>{self}</tg-spoiler>')
    
    @classmethod
    def to_list(cls, items: list[str], type: str = 'num', sep: str = '\n', type_list: list[str] | None = None) -> "TextHTML":
        ''' Нумерованный список
            - items: Список элементов 
            - type: Тип списка (num - нумерованный, любой другой - кастомный символ)
            - sep: Разделитель между элементами списка '''
        if type == 'num':
            return cls(sep.join([f'{i+1}. {item}' for i, item in enumerate(items)]))
        elif type == 'bullet':
            return cls(sep.join([f'• {item}' for item in items]))
        elif type == 'list' and type_list:
            return cls(sep.join([f'{type_list[i]} {item}' for i, item in enumerate(items)]))
        else:
            return cls(sep.join([f'{type} {item}' for item in items]))
        
    @classmethod
    def num_list(cls, items: list[str], sep: str = '\n') -> "TextHTML":
        ''' Нумерованный список
            - items: Список элементов для нумерации
            - sep: Разделитель между элементами списка '''
        return cls.to_list(items, type='num', sep=sep)
    
    @staticmethod
    def float_format(value: float | int, decimals: int = 2) -> "TextHTML":
        """Форматирует число без лишних нулей"""
        formatted = f"{value:.{decimals}f}"
        return TextHTML(formatted.rstrip('0').rstrip('.'))
    
    @staticmethod
    def json_format(json_data: dict, indent: int = 2) -> "TextHTML":
        """Форматирует json с отступами
            - json_data: Данные для форматирования
            - indent: Количество отступов"""
        return TextHTML(json.dumps(json_data, ensure_ascii=False, indent=indent).encode('utf-8').decode('utf-8'))

    def pre(self, language: str = 'python') -> "TextHTML":
        """Преобразует текст в блок кода
            - language: Язык программирования"""
        return TextHTML(f'<pre><code class="language-{language}">{self}</code></pre>')

    def openmessage(self, user_id: int) -> "TextHTML":
        """Ссылку на чат с пользователем
            - user_id: Telegram ID пользователя"""
        return TextHTML(f'<a href="tg://user?id={user_id}">{self}</a>')
    
    def to_html(self) -> "TextHTML":
        """Преобразует markdown в html"""
        return TextHTML(markdown.markdown(self))

    def strip_html(self) -> "TextHTML":
        """Удаляет HTML теги"""
        stripper = HTMLStripper()
        stripper.feed(self)
        return stripper.get_data()
    
    @classmethod
    def example(cls) -> "TextHTML":
        return cls(open('.\\app\\aio\\cls\\msg\\rich_example.html', 'r', encoding='UTF-8').read())

    def details(self, title: str = 'Открыть', is_close: bool = True) -> "TextHTML":
        """ Сворачиваемый блок 
            - title: Заголовок 
            - is_close: Изначально закрытый"""
        return TextHTML(f'<details {'close' if is_close else 'open'}><summary>{title}</summary>{self}</details>')

    def headers(self, num: int = 1) -> "TextHTML":
        """ Заголовок
            - num: Уровень заголовка """
        return TextHTML(f'<h{num}>{self}</h{num}>')

    @property
    def h1(self):
        return self.headers(1)
    
    @property
    def h2(self):
        return self.headers(2)
    
    @property
    def h3(self):
        return self.headers(3)
    
    @property
    def h4(self):
        return self.headers(4)
    
    @property
    def h5(self):
        return self.headers(5)
    
    @property
    def h6(self):
        return self.headers(6)

    def paragraf(self) -> "TextHTML":
        """Параграф"""
        return TextHTML(f'<p>{self}</p>')

    def mark(self) -> "TextHTML":
        """Выделить"""
        return TextHTML(f'<mark>{self}</mark>')
    
    def aside(self, cite: str | None = None) -> "TextHTML":
        """ Выделенная Цитата 
            - cite: Автор цитаты"""
        return TextHTML(f'<aside>{self}{f'<cite>{cite}</cite>' if cite else ''}</aside>')
    
    def hr(self, to_front: bool = False) -> "TextHTML":
        """ Разделитель 
            - to_front: Спереди текста"""
        return TextHTML(f'<hr>{self}') if to_front else TextHTML(f'{self}<hr>')
    
    @classmethod
    def anchor(cls, name: str):
        return cls(f'<a name="{name}"></a>')
    
    @property
    def br(self):
        return TextHTML(f'{self}<br>')

    @classmethod
    def joined(cls, iter: list, sep: str = '<br>'):
        return cls(sep.join(iter))

class TextHTML(TextHTMLBase):
    # ─── Методы изменения регистра ──────────────────────────────────

    def upper(self) -> "TextHTML":
        """Преобразовать строку в ПРОПИСНЫЕ БУКВЫ"""
        return TextHTML(super().upper())
    
    def lower(self) -> "TextHTML":
        """Преобразовать строку в строчные буквы"""
        return TextHTML(super().lower())
    
    def capitalize(self) -> "TextHTML":
        """Первый символ в прописную букву, остальные в строчные"""
        return TextHTML(super().capitalize())
    
    def title(self) -> "TextHTML":
        """Первый символ каждого слова в прописную букву"""
        return TextHTML(super().title())
    
    def swapcase(self) -> "TextHTML":
        """Поменять регистр букв на противоположный"""
        return TextHTML(super().swapcase())
    
    def casefold(self) -> "TextHTML":
        """Преобразовать в строку, пригодную для сравнения без учёта регистра"""
        return TextHTML(super().casefold())

    # ─── Методы замены и удаления ────────────────────────────────────

    def replace(self, old: str, new: str, count: int = -1) -> "TextHTML":
        """Заменить вхождения подстроки на новую подстроку
        - old: строка для замены
        - new: новая строка
        - count: максимальное количество замен (-1 = все)"""
        return TextHTML(super().replace(old, new, count))

    def strip(self, chars: str | None = None) -> "TextHTML":
        """Удалить пробелы (или указанные символы) с обеих сторон"""
        return TextHTML(super().strip(chars))
    
    def lstrip(self, chars: str | None = None) -> "TextHTML":
        """Удалить пробелы (или указанные символы) слева"""
        return TextHTML(super().lstrip(chars))
    
    def rstrip(self, chars: str | None = None) -> "TextHTML":
        """Удалить пробелы (или указанные символы) справа"""
        return TextHTML(super().rstrip(chars))

    def removeprefix(self, prefix: str) -> "TextHTML":
        """Удалить префикс из начала строки, если он есть"""
        return TextHTML(super().removeprefix(prefix))
    
    def removesuffix(self, suffix: str) -> "TextHTML":
        """Удалить суффикс из конца строки, если он есть"""
        return TextHTML(super().removesuffix(suffix))

    # ─── Методы выравнивания и заполнения ────────────────────────────

    def ljust(self, width: int, fillchar: str = ' ') -> "TextHTML":
        """Выравнять строку влево на ширину width с заполнением fillchar"""
        return TextHTML(super().ljust(width, fillchar))
    
    def rjust(self, width: int, fillchar: str = ' ') -> "TextHTML":
        """Выравнять строку вправо на ширину width с заполнением fillchar"""
        return TextHTML(super().rjust(width, fillchar))
    
    def center(self, width: int, fillchar: str = ' ') -> "TextHTML":
        """Выравнять строку по центру на ширину width с заполнением fillchar"""
        return TextHTML(super().center(width, fillchar))
    
    def zfill(self, width: int) -> "TextHTML":
        """Заполнить нулями слева до ширины width (для чисел)"""
        return TextHTML(super().zfill(width))

    def expandtabs(self, tabsize: int = 8) -> "TextHTML":
        """Заменить табуляции на пробелы (табстоп по умолчанию 8)"""
        return TextHTML(super().expandtabs(tabsize))

    # ─── Методы для списков и объединения ──────────────────────────

    def join(self, iterable: list[str] | tuple[str, ...]) -> "TextHTML":
        """Объединить элементы итерируемого объекта текущей строкой как разделитель"""
        return TextHTML(super().join(iterable))

    def split(self, sep: str | None = None, maxsplit: int = -1) -> list["TextHTML"]:
        """Разделить строку на подстроки"""
        result = super().split(sep, maxsplit)
        return [TextHTML(item) for item in result]

    def rsplit(self, sep: str | None = None, maxsplit: int = -1) -> list["TextHTML"]:
        """Разделить строку на подстроки (справа)"""
        result = super().rsplit(sep, maxsplit)
        return [TextHTML(item) for item in result]

    def splitlines(self, keepends: bool = False) -> list["TextHTML"]:
        """Разделить строку по строкам"""
        result = super().splitlines(keepends)
        return [TextHTML(item) for item in result]

    def partition(self, sep: str) -> tuple["TextHTML", "TextHTML", "TextHTML"]:
        """Разбить строку на три части"""
        left, middle, right = super().partition(sep)
        return TextHTML(left), TextHTML(middle), TextHTML(right)

    def rpartition(self, sep: str) -> tuple["TextHTML", "TextHTML", "TextHTML"]:
        """Разбить строку на три части (справа)"""
        left, middle, right = super().rpartition(sep)
        return TextHTML(left), TextHTML(middle), TextHTML(right)

    # ─── Методы поиска ──────────────────────────────────────────────

    def find(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Найти подстроку (слева)"""
        if end == -1:
            return super().find(sub, start)
        return super().find(sub, start, end)

    def rfind(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Найти подстроку (справа)"""
        if end == -1:
            return super().rfind(sub, start)
        return super().rfind(sub, start, end)

    def index(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Найти индекс подстроки (слева)"""
        if end == -1:
            return super().index(sub, start)
        return super().index(sub, start, end)

    def rindex(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Найти индекс подстроки (справа)"""
        if end == -1:
            return super().rindex(sub, start)
        return super().rindex(sub, start, end)

    def count(self, sub: str, start: int = 0, end: int = -1) -> int:
        """Подсчитать количество вхождений подстроки"""
        if end == -1:
            return super().count(sub, start)
        return super().count(sub, start, end)

    # ─── Методы проверки ────────────────────────────────────────────

    def startswith(self, prefix: str | tuple[str, ...], start: int = 0, end: int = -1) -> bool:
        """Проверить начало строки"""
        if end == -1:
            return super().startswith(prefix, start)
        return super().startswith(prefix, start, end)

    def endswith(self, suffix: str | tuple[str, ...], start: int = 0, end: int = -1) -> bool:
        """Проверить конец строки"""
        if end == -1:
            return super().endswith(suffix, start)
        return super().endswith(suffix, start, end)

    def isalpha(self) -> bool:
        """Проверить, содержит ли только буквы"""
        return super().isalpha()

    def isdigit(self) -> bool:
        """Проверить, содержит ли только цифры"""
        return super().isdigit()

    def isnumeric(self) -> bool:
        """Проверить, содержит ли только числовые символы"""
        return super().isnumeric()

    def isalnum(self) -> bool:
        """Проверить, содержит ли только буквы и цифры"""
        return super().isalnum()

    def isspace(self) -> bool:
        """Проверить, содержит ли только пробелы"""
        return super().isspace()

    def isupper(self) -> bool:
        """Проверить, написана ли строка заглавными буквами"""
        return super().isupper()

    def islower(self) -> bool:
        """Проверить, написана ли строка строчными буквами"""
        return super().islower()

    def istitle(self) -> bool:
        """Проверить, написана ли строка в заголовочном формате"""
        return super().istitle()

    def isidentifier(self) -> bool:
        """Проверить, является ли строка валидным идентификатором"""
        return super().isidentifier()

    def isdecimal(self) -> bool:
        """Проверить, содержит ли только десятичные символы"""
        return super().isdecimal()

    # ─── Методы форматирования ──────────────────────────────────────

    def format(self, *args: Any, **kwargs: Any) -> "TextHTML":
        """Форматировать строку подставляя позиционные и именованные аргументы"""
        return TextHTML(super().format(*args, **kwargs))
    
    def format_map(self, mapping: dict) -> "TextHTML":
        """Форматировать строку используя словарь"""
        return TextHTML(super().format_map(mapping))

    def translate(self, table: dict) -> "TextHTML":
        """Заменить символы согласно таблице трансляции"""
        return TextHTML(super().translate(table))

    # ─── Операторы ──────────────────────────────────────────────────

    def __add__(self, other: str) -> "TextHTML":
        """Оператор + для конкатенации строк"""
        if isinstance(other, str):
            return TextHTML(super().__add__(other))
        return NotImplemented

    def __radd__(self, other: str) -> "TextHTML":
        """Оператор + для конкатенации (правый операнд)"""
        if isinstance(other, str):
            return TextHTML(other.__add__(self))
        return NotImplemented

    def __mul__(self, n: int) -> "TextHTML":
        """Оператор * для повторения строки n раз"""
        return TextHTML(super().__mul__(n))
    
    def __rmul__(self, n: int) -> "TextHTML":
        """Оператор * для повторения строки n раз (правый операнд)"""
        return TextHTML(super().__rmul__(n))

    def __mod__(self, other: Any) -> "TextHTML":
        """Оператор % для форматирования строки"""
        return TextHTML(super().__mod__(other))
    
    def __rmod__(self, other: str) -> "TextHTML":
        """Оператор % для форматирования строки (правый операнд)"""
        if isinstance(other, str):
            return TextHTML(other.__mod__(self))
        return NotImplemented

    # ─── Срезы и индексация ─────────────────────────────────────────

    def __getitem__(self, index: int | slice) -> "TextHTML":
        """Получить символ или подстроку по индексу или срезу"""
        result = super().__getitem__(index)
        if isinstance(result, str) and not isinstance(result, TextHTML):
            return TextHTML(result)
        return result

    def __getslice__(self, start: int, end: int) -> "TextHTML":
        """Получить подстроку по срезу (устаревшее, используйте __getitem__)"""
        result = super().__getslice__(start, end)
        if isinstance(result, str) and not isinstance(result, TextHTML):
            return TextHTML(result)
        return result

def get_invisibly_edited():
    return str('\u200b'*random.choice(range(10)))   

