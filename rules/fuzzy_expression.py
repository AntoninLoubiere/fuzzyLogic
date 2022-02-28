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


def fe_name(var: LinguisticVariable, name: str) -> FuzzyExpression:
    val = var.value_from_name(name)
    return FuzzyExpression(var, val) if val else None
