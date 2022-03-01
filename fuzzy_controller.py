from __future__ import annotations

from os import PathLike
from typing import Optional

import yaml

from fuzzy_parser import assert_type, dict_el, dict_loop, list_loop, ParseInfo
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

    @classmethod
    def load_from_file(cls, file_path: str | PathLike[str]) -> 'FuzzyController':
        with open(file_path) as fir:
            data: dict = yaml.load(fir, yaml.FullLoader)

        assert_type(data, dict)
        parse_info = ParseInfo(
            version=dict_el(data, 'version', int, 0),
            type=dict_el(data, 'type', str, 'linear')
        )

        result = cls()

        variables = dict_el(data, 'variables', dict, {})
        for name, var in dict_loop(variables, dict):
            result.add_variable(LinguisticVariable.load_from_data(parse_info, name, var))

        rules = dict_el(data, 'rules', list, [])
        for rule in list_loop(rules, dict):
            result.add_rule(FuzzyRule.load_from_data(parse_info, result.variables, rule))

        return result
