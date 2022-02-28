import unittest

from fuzzy_sets.linear_fuzzy_set_helpers import left_trapeze_set, trapeze_set, right_trapeze_set
from rules.variables import LinguisticVariable

from rules.values import LinguisticValue


class TestLinguisticVariable(unittest.TestCase):

    def setUp(self) -> None:
        self.cold = LinguisticValue("Cold", left_trapeze_set(0, 30, 10, 12))
        self.fresh = LinguisticValue("Fresh", trapeze_set(0, 30, 10, 12, 15, 17))
        self.good = LinguisticValue("Good", trapeze_set(0, 30, 15, 17, 20, 25))
        self.hot = LinguisticValue("Hot", right_trapeze_set(0, 30, 20, 28))
        self.variable = LinguisticVariable("Temperature", [
            self.cold,
            self.fresh,
            self.good,
            self.hot,
        ])

    def test_linguistic_variable(self):
        self.assertEqual(self.variable.name, "Temperature")
        self.assertIs(self.variable.values[0], self.cold)
        self.assertIs(self.variable.values[1], self.fresh)
        self.assertIs(self.variable.values[2], self.good)
        self.assertIs(self.variable.values[3], self.hot)

        self.assertIs(self.variable.value_from_name("Cold"), self.cold)
        self.assertIs(self.variable.value_from_name("Fresh"), self.fresh)
        self.assertIsNone(self.variable.value_from_name("fresh"))
        self.assertIsNone(self.variable.value_from_name("Don't exist"))


class TestLinguisticValues(unittest.TestCase):

    def test_linguistic(self):
        s = trapeze_set(1, 6, 2, 3, 4, 5)
        value = LinguisticValue("Name", s)

        self.assertEqual(value.name, "Name")
        self.assertEqual(value.set, s)
        self.assertEqual(value.belongs_value(3.5), s.belongs_value(3.5))


if __name__ == '__main__':
    unittest.main()
