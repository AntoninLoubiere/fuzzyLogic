import math

from fuzzy_sets.fuzzy_set import BaseFuzzySet
from rules.fuzzy_expression import FuzzyExpression


class FuzzyRule:
    def __init__(self, premises: list[FuzzyExpression], conclusions: list[FuzzyExpression]):
        self.premises = premises
        self.conclusions = conclusions

    def apply(self, data: dict[str, float]) -> dict[str, BaseFuzzySet]:
        degree = math.inf
        for p in self.premises:
            name = p.variable.name
            if name in data:
                deg = p.value.belongs_value(data[name])
                if deg < degree:
                    degree = deg
            else:
                return {c.variable.name: c.value.set * 0 for c in self.conclusions}

        if degree:
            return {c.variable.name: c.value.set * degree for c in self.conclusions}
        else:
            return {c.variable.name: c.value.set * degree for c in self.conclusions}

    def __str__(self):
        return ' AND '.join((str(p) for p in self.premises)) + " THEN " + 'AND'.join((str(c) for c in self.conclusions))

    def __repr__(self):
        return self.__str__()
