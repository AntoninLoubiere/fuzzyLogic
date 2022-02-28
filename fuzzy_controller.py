from typing import Optional

from fuzzy_sets.fuzzy_set import BaseFuzzySet
from rules.rules import FuzzyRule
from rules.variables import LinguisticVariable

class FuzzyController:

    def __init__(self, variables: Optional[list[LinguisticVariable]] = None,
                 rules: Optional[list[FuzzyRule]] = None):
        variables = variables if variables else []
        self.variables: dict[str, LinguisticVariable] = {v.name: v for v in variables}
        self.rules = rules if rules else []

    def add_variable(self, variable: LinguisticVariable) -> None:
        self.variables[variable.name] = variable

    def remove_variable(self, variable: LinguisticVariable) -> None:
        del self.variables[variable.name]

    def add_rule(self, rule: FuzzyRule) -> None:
        self.rules.append(rule)

    def remove_rule(self, rule: FuzzyRule) -> None:
        self.rules.remove(rule)

    def resolve(self, data: dict[str, float]) -> dict[str, float]:
        results: dict[str, BaseFuzzySet] = {}
        for r in self.rules:
            d = r.apply(data)
            for key in d:
                if key not in results:
                    results[key] = d[key]
                else:
                    results[key] |= d[key]

        return {k: results[k].barycenter() for k in results}

    def __str__(self):
        return f"{self.rules}"

    def __repr__(self):
        return f"<FuzzyController rules={self.rules}; variables={self.variables}>"
