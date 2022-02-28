import unittest

from fuzzy_sets.linear_fuzzy_set_helpers import left_trapeze_set, trapeze_set, right_trapeze_set
from rules.fuzzy_expression import fe_name
from rules.rules import FuzzyRule
from rules.values import LinguisticValue
from rules.variables import LinguisticVariable
from fuzzy_controller import FuzzyController


class TestFuzzyController(unittest.TestCase):

    def setUp(self):
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
        self.rule1 = FuzzyRule([fe_name(self.temperature, 'cold')], [fe_name(self.store_height, 'up')])
        self.rule2 = FuzzyRule(
            [fe_name(self.temperature, 'good'), fe_name(self.luminosity, 'dark')], [fe_name(self.store_height, 'up')])
        self.rule3 = FuzzyRule(
            [fe_name(self.temperature, 'good'), fe_name(self.luminosity, 'medium')],
            [fe_name(self.store_height, 'medium')])
        self.rule4 = FuzzyRule(
            [fe_name(self.temperature, 'good'), fe_name(self.luminosity, 'light')],
            [fe_name(self.store_height, 'down')])

        self.controller = FuzzyController([self.temperature], [self.rule1])
        self.controller.add_variable(self.luminosity)
        self.controller.add_variable(self.store_height)

        self.controller.add_rule(self.rule2)
        self.controller.add_rule(self.rule3)
        self.controller.add_rule(self.rule4)

    def test_controller(self):
        self.assertEqual(self.controller.rules, [self.rule1, self.rule2, self.rule3, self.rule4])
        self.assertEqual(self.controller.variables,  {
            'temperature': self.temperature,
            'luminosity': self.luminosity,
            'store_height': self.store_height
        })

    def test_resolve(self):
        self.assertEqual(self.controller.resolve(
            {'temperature': 9, 'luminosity': 100_000}
        ), {'store_height': 98})

        self.assertEqual(self.controller.resolve(
            {'temperature': 16, 'luminosity': 24_000}
        ), {'store_height': 68.52931648850017})


if __name__ == '__main__':
    unittest.main()
