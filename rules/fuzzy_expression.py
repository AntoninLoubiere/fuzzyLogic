from fuzzy_parser import parse_assert, ParseInfo
from rules.values import LinguisticValue
from rules.variables import LinguisticVariable


class FuzzyExpression:

    def __init__(self, var: LinguisticVariable, val: LinguisticValue):
        self.variable = var
        self.value = val

    def __eq__(self, other):
        return self.variable == other.variable and self.value == other.value

    def __str__(self):
        return f"{self.variable.name}={self.value.name}"

    def __repr__(self):
        return f"<FuzzyExpression {self.variable.name}={self.value.name}>"

    @classmethod
    def load_from_data(cls, parse_info: ParseInfo, variables: dict[str, LinguisticVariable], name: str, value: str):
        parse_assert(name in variables, f"The variable {name} hasn't been declared.")
        var = variables[name]
        val = var.value_from_name(value)
        parse_assert(val is not None, f"The value {value} doesn't exist in {name}.")
        return cls(var, val)


def fe_name(var: LinguisticVariable, name: str) -> FuzzyExpression:
    val = var.value_from_name(name)
    return FuzzyExpression(var, val) if val else None
