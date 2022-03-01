from collections import namedtuple
from typing import Any

ParseInfo = namedtuple('ParseInfo', ['version', 'type'])


class ParsingException(BaseException):
    pass


def assert_type(data: Any, type_excepted: type) -> None:
    if not isinstance(data, type_excepted):
        raise ParsingException('The data is malformed !')


def dict_el(data: dict[str], sub_element: str, type_excepted: type, default_value=None):
    value = data.get(sub_element, default_value)
    if not isinstance(value, type_excepted):
        raise ParsingException(f'The field "{sub_element}" should be a "{type_excepted}" not a {type(data)}.')

    return value


def dict_loop(data: dict, type_excepted: type):
    for key in data:
        d = data[key]
        if not isinstance(d, type_excepted):
            raise ParsingException(f'The item {key} should have a type of {type_excepted}.')
        yield key, d


def list_loop(data: list, type_excepted: type):
    for e in data:
        if not isinstance(e, type_excepted):
            raise ParsingException(f'This item should have a type of {type_excepted}.')
        yield e


def parse_assert(condition: bool, message: str = "An error occurred while parsing the controller.") -> None:
    if not condition:
        raise ParsingException(message)


def parse_set(parse_info: ParseInfo, data: str) -> 'BaseFuzzySet':
    from fuzzy_sets.linear_fuzzy_set import LinearFuzzySet
    if parse_info.type == 'linear':
        return LinearFuzzySet.load_from_data(data)
    else:
        raise ParsingException(f'The type {parse_info.type} is unknown.')
