import unittest

from fuzzy_sets.linear_fuzzy_set import LinearFuzzySet
from fuzzy_sets.linear_fuzzy_set_helpers import left_trapeze_set, trapeze_set, right_trapeze_set, constant_set
from rules.values import LinguisticValue
from rules.variables import LinguisticVariable

from rules.fuzzy_expression import FuzzyExpression, fe_name
from rules.rules import FuzzyRule


class TestFuzzyRules(unittest.TestCase):

    def setUp(self) -> None:
        self.temperature = LinguisticVariable("temperature", [
            LinguisticValue("cold", left_trapeze_set(0, 30, 10, 12)),
            LinguisticValue("fresh", trapeze_set(0, 30, 10, 12, 15, 17)),
            LinguisticValue("good", trapeze_set(0, 30, 15, 17, 20, 25)),
            LinguisticValue("hot", right_trapeze_set(0, 30, 20, 28))
        ])

        self.luminosity = LinguisticVariable("luminosity", [
            LinguisticValue("dark", left_trapeze_set(0, 100_000, 20_000, 30_000)),
            LinguisticValue("medium", trapeze_set(0, 100_000, 20_000, 30_000, 60_000, 85_000)),
            LinguisticValue("light", right_trapeze_set(0, 100_000, 60_000, 85_000))
        ])

        self.store_height = LinguisticVariable("store_height", [
            LinguisticValue("down", left_trapeze_set(0, 105, 25, 40)),
            LinguisticValue("medium", trapeze_set(0, 105, 25, 40, 85, 100)),
            LinguisticValue("up", right_trapeze_set(0, 105, 85, 100))
        ])
        self.premise1 = FuzzyExpression(self.temperature, self.temperature.values[2])
        self.premise2 = fe_name(self.luminosity, "light")
        self.conclusion = fe_name(self.store_height, 'down')
        self.rule = FuzzyRule([self.premise1, self.premise2], [self.conclusion])

    def test_fuzzy_rules(self):
        self.assertEqual(self.premise1, fe_name(self.temperature, "good"))

        self.assertEqual(self.rule.premises, [self.premise1, self.premise2])
        self.assertEqual(self.rule.conclusions, [self.conclusion])

    def test_apply(self):
        empty_set = constant_set(self.rule.conclusions[0].value.set.min, self.rule.conclusions[0].value.set.max, 0)
        self.assertEqual(self.rule.apply({'temperature': 16, 'luminosity': 85_000}), {'store_height': self.conclusion.value.set * .5})
        self.assertEqual(self.rule.apply({'temperature': 16, 'luminosity': 10_000}), {'store_height': empty_set})
        self.assertEqual(self.rule.apply({'temperature': 16}), {'store_height': empty_set})


if __name__ == '__main__':
    unittest.main()
