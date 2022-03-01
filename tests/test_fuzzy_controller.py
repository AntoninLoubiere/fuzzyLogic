import unittest

from fuzzy_controller import FuzzyController
from fuzzy_sets.linear_fuzzy_set_helpers import left_trapeze_set, right_trapeze_set, trapeze_set
from points import Point
from rules.fuzzy_expression import fe_name
from rules.rules import FuzzyRule
from rules.values import LinguisticValue
from rules.variables import LinguisticVariable


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
        self.assertEqual(self.controller.variables, {
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


class TestFuzzyControllerImport(unittest.TestCase):

    def test_import(self):
        controller = FuzzyController.load_from_file('./fuzzy_controller.fzc')
        self.assertEqual(len(controller.variables), 3)
        self.assertIn('temperature', controller.variables)
        self.assertIn('luminosity', controller.variables)
        self.assertIn('store_height', controller.variables)
        temp = controller.variables['temperature']
        self.assertEqual(temp.min, 0)
        self.assertEqual(temp.max, 30)
        self.assertEqual(temp.values[0].name, 'cold')
        self.assertEqual(temp.values[1].name, 'fresh')
        self.assertEqual(temp.values[2].name, 'good')
        self.assertEqual(temp.values[3].name, 'hot')
        self.assertEqual(temp.values[0].set.points[0], Point(10, 1))

        self.assertEqual(len(controller.rules), 10)

        rule = controller.rules[0]
        self.assertEqual(len(rule.premises), 1)
        self.assertEqual(len(rule.conclusions), 1)

        rule = controller.rules[2]
        self.assertEqual(rule.premises[0].variable.name, 'temperature')
        self.assertEqual(rule.premises[0].value.name, 'fresh')
        self.assertEqual(rule.premises[1].variable.name, 'luminosity')
        self.assertEqual(rule.premises[1].value.name, 'medium')
        self.assertEqual(rule.conclusions[0].variable.name, 'store_height')
        self.assertEqual(rule.conclusions[0].value.name, 'up')


if __name__ == '__main__':
    unittest.main()
