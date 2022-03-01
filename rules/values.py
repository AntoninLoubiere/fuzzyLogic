from fuzzy_parser import parse_set, ParseInfo
from fuzzy_sets.fuzzy_set import BaseFuzzySet


class LinguisticValue:
    def __init__(self, name: str, fuzzy_set: BaseFuzzySet):
        self.name = name
        self.set = fuzzy_set

    def belongs_value(self, x: float) -> float:
        return self.set.belongs_value(x)

    def __eq__(self, other):
        return other.name == self.name

    def __str__(self):
        return "value=" + self.name

    def __repr__(self):
        return f"<LinguisticValue name={self.name}; set={self.set}>"

    @classmethod
    def load_from_data(cls, parse_info: ParseInfo, name: str, data: str) -> 'LinguisticValue':
        result = cls(name, parse_set(parse_info, data))
        return result
