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
