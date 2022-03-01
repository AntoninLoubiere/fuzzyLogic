import math

from fuzzy_parser import dict_el, dict_loop, ParseInfo
from fuzzy_sets.fuzzy_set import BaseFuzzySet
from rules.fuzzy_expression import FuzzyExpression
from rules.variables import LinguisticVariable


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

        return {c.variable.name: c.value.set * degree for c in self.conclusions}

    def __str__(self):
        return ' AND '.join((str(p) for p in self.premises)) + " THEN " + 'AND'.join((str(c) for c in self.conclusions))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def load_from_data(cls, pi: ParseInfo, vars: dict[str, LinguisticVariable], data: dict) -> 'FuzzyRule':
        return cls(
            [FuzzyExpression.load_from_data(pi, vars, name, value) for name, value in
             dict_loop(dict_el(data, 'conditions', dict), str)],
            [FuzzyExpression.load_from_data(pi, vars, name, value) for name, value in
             dict_loop(dict_el(data, 'actions', dict), str)]
        )
