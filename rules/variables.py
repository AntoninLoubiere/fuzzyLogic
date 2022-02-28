from typing import Optional

from rules.values import LinguisticValue


class LinguisticVariable:
    def __init__(self, name: str, values: list[LinguisticValue]):
        self.name = name
        self.values = values
        self.min = min(self.values, key=lambda v: v.set.min).set.min
        self.max = min(self.values, key=lambda v: v.set.max).set.max

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
