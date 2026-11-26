import json5
import re
from typing import Any


def values_by_tag(groups) -> dict[str, Any]:
    return {
        parameter.tag: parameter.value
        for group in groups
        for parameter in group.parametrs
    }


def is_setting_available(parameter, values: dict[str, Any]) -> bool:
    for dependency in getattr(parameter, 'depends_on', None) or []:
        tag = dependency.tag
        if tag not in values:
            return False
        current = values[tag]
        expected = dependency.value
        operator = dependency.operator
        if operator == 'equals' and current != expected:
            return False
        if operator == 'not_equals' and current == expected:
            return False
        if operator == 'in' and current not in (expected if isinstance(expected, (list, tuple, set)) else [expected]):
            return False
        if operator == 'not_in' and current in (expected if isinstance(expected, (list, tuple, set)) else [expected]):
            return False
        if operator not in {'equals', 'not_equals', 'in', 'not_in'}:
            return False
    return True


def coerce_setting_input(raw_value: str, parameter) -> Any:
    type_name = (getattr(parameter, 'type_', None) or '').strip().lower()
    aliases = {
        'string': 'str',
        'integer': 'int',
        'long': 'int',
        'number': 'float',
        'double': 'float',
        'boolean': 'bool',
        'object': 'dict',
        'array': 'list',
    }
    type_name = aliases.get(type_name, type_name)

    supported_types = {'str', 'text', 'int', 'float', 'bool', 'dict', 'list', 'json'}
    if type_name not in supported_types:
        example_value = getattr(parameter, 'value', None)
        if example_value is None:
            example_value = getattr(parameter, 'default_value', None)
        if isinstance(example_value, bool):
            type_name = 'bool'
        elif isinstance(example_value, int):
            type_name = 'int'
        elif isinstance(example_value, float):
            type_name = 'float'
        elif isinstance(example_value, dict):
            type_name = 'dict'
        elif isinstance(example_value, list):
            type_name = 'list'
        else:
            min_value = getattr(parameter, 'min_value', None)
            max_value = getattr(parameter, 'max_value', None)
            if any(value is not None for value in (min_value, max_value)):
                type_name = 'int' if all(
                    value is None or isinstance(value, int) and not isinstance(value, bool)
                    for value in (min_value, max_value)
                ) else 'float'
            else:
                # For top-level settings, API `type` names the settings family
                # (such as "organ"), so infer string for nullable text fields.
                type_name = 'str'

    if type_name in {'str', 'text'}:
        value = raw_value
    elif type_name == 'int':
        try:
            value = int(raw_value.strip())
        except ValueError as error:
            raise ValueError('Введите целое число.') from error
    elif type_name == 'float':
        try:
            value = float(raw_value.strip())
        except ValueError as error:
            raise ValueError('Введите число.') from error
    elif type_name == 'bool':
        normalized = raw_value.strip().casefold()
        true_values = {'true', '1', 'yes', 'да', 'вкл', 'включено'}
        false_values = {'false', '0', 'no', 'нет', 'выкл', 'выключено'}
        if normalized in true_values:
            value = True
        elif normalized in false_values:
            value = False
        else:
            raise ValueError('Введите true/false, да/нет или вкл/выкл.')
    elif type_name in {'dict', 'list', 'json'}:
        try:
            value = json5.loads(raw_value)
        except (ValueError, TypeError) as error:
            raise ValueError('Введите корректное значение в формате JSON.') from error
        if type_name == 'dict' and not isinstance(value, dict):
            raise ValueError('Ожидается JSON-объект.')
        if type_name == 'list' and not isinstance(value, list):
            raise ValueError('Ожидается JSON-массив.')
    else:
        raise ValueError(f'Неизвестный тип настройки: {type_name or "не указан"}.')

    min_value = getattr(parameter, 'min_value', None)
    max_value = getattr(parameter, 'max_value', None)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if min_value is not None and value < min_value:
            raise ValueError(f'Минимальное значение: {min_value}.')
        if max_value is not None and value > max_value:
            raise ValueError(f'Максимальное значение: {max_value}.')

    min_length = getattr(parameter, 'min_length', None)
    max_length = getattr(parameter, 'max_length', None)
    if isinstance(value, (str, list, dict)):
        if min_length is not None and len(value) < min_length:
            raise ValueError(f'Минимальная длина: {min_length}.')
        if max_length is not None and len(value) > max_length:
            raise ValueError(f'Максимальная длина: {max_length}.')

    pattern = getattr(parameter, 'pattern', None)
    if isinstance(value, str) and pattern and re.fullmatch(pattern, value) is None:
        raise ValueError('Значение не соответствует требуемому формату.')
    return value
