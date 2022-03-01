from typing import Optional, Union

from fuzzy_parser import dict_el, dict_loop, ParseInfo
from rules.values import LinguisticValue


class LinguisticVariable:
    def __init__(self, name: str, values: list[LinguisticValue]):
        self.name = name
        self.values = values
        self.min = min(self.values, key=lambda v: v.set.min).set.min if self.values else 0
        self.max = min(self.values, key=lambda v: v.set.max).set.max if self.values else 0

    def value_from_name(self, name: str) -> Optional[LinguisticValue]:
        for v in self.values:
            if v.name == name:
                return v

        return None

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return "var=" + self.name

    def __repr__(self):
        return f"<LinguisticVariable name={self.name}; values={self.values}; min={self.min}; max={self.max}>"

    @classmethod
    def load_from_data(cls, parse_info: ParseInfo, variable_name: str, data: dict) -> 'LinguisticVariable':
        result = cls(variable_name, [])

        result.min = dict_el(data, 'min', Union[int, float])
        result.max = dict_el(data, 'max', Union[int, float])

        values = dict_el(data, 'values', dict)

        for name, val in dict_loop(values, str):
            result.values.append(LinguisticValue.load_from_data(parse_info, name, val))

        return result
