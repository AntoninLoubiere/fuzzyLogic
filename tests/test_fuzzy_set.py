import unittest
from itertools import zip_longest

from fuzzy_sets import fuzzy_set, linear_fuzzy_set, linear_fuzzy_set_helpers
from points import Point


class TestFuzzySet(unittest.TestCase):

    def setUp(self):
        self.f_set = fuzzy_set.BaseFuzzySet(1, 10)
        self.f_set.add_point(Point(1, 0))
        self.f_set.add_point(Point(2, 0))
        self.f_set.add_point(Point(4, 1))
        self.f_set.add_point(Point(6, 1))
        self.f_set.add_point(Point(8, 0))
        self.f_set.add_point(Point(10, 0))

    def test_fuzzy_set(self):
        f_set = fuzzy_set.BaseFuzzySet(1, 10)
        self.assertEqual(f_set.min, 1)
        self.assertEqual(f_set.max, 10)
        self.assertEqual(f_set.points, [])

    def test_add_points(self):
        f_set = fuzzy_set.BaseFuzzySet(1, 10)

        p1 = Point(1, 0)
        f_set.add_point(p1)
        self.assertEqual(f_set.points, [p1])

        p4 = Point(4, 1)
        f_set.add_point(p4)
        self.assertEqual(f_set.points, [p1, p4])

        p3 = Point(3, 0.25)
        f_set.add_point(p3)
        self.assertEqual(f_set.points, [p1, p3, p4])

        p5 = f_set.add_point_from_coord(5, 1)
        self.assertEqual(f_set.points, [p1, p3, p4, p5])

        p2 = f_set.add_point_from_coord(2, 0.1)
        self.assertEqual(f_set.points, [p1, p2, p3, p4, p5])

    def test_get_point_index(self):
        self.assertEqual(self.f_set.get_index_from_point(1.5), 1)
        self.assertEqual(self.f_set.get_index_from_point(5), 3)
        self.assertEqual(self.f_set.get_index_from_point(7), 4)
        self.assertEqual(self.f_set.get_index_from_point(8), 5)
        self.assertEqual(self.f_set.get_index_from_point(11), 6)

    def test_equals(self):
        f_set = fuzzy_set.BaseFuzzySet(1, 10)
        f_set.add_point(Point(1, 0))
        f_set.add_point(Point(2, 0))
        f_set.add_point(Point(4, 1))
        f_set.add_point(Point(6, 1))
        f_set.add_point(Point(10, 0))
        f_set.add_point(Point(8, 0))
        self.assertTrue(self.f_set == f_set)

        f_set.min = 3
        self.assertFalse(self.f_set == f_set)
        f_set.min = 1
        self.assertFalse(self.f_set != f_set)
        f_set.points[2] *= .9
        self.assertTrue(self.f_set != f_set)
        f_set.points[2] *= 1 / .9
        self.assertFalse(self.f_set != f_set)
        f_set.points[2].x *= .9
        self.assertTrue(self.f_set != f_set)
        f_set.points[2].x *= 1 / .9
        self.assertFalse(self.f_set != f_set)

    def test_not(self):
        f_set = fuzzy_set.BaseFuzzySet(1, 10)
        f_set.add_point(Point(1, 1))
        f_set.add_point(Point(2, 1))
        f_set.add_point(Point(4, 0))
        f_set.add_point(Point(6, 0))
        f_set.add_point(Point(10, 1))
        f_set.add_point(Point(8, 1))

        self.assertEqual(f_set, self.f_set.not_operator())

    def test_multiply(self):
        f_set = self.f_set * 0.2
        for p1, p2 in zip_longest(self.f_set.points, f_set.points):
            self.assertEqual(p1 * 0.2, p2)

        self.f_set *= 0.2
        self.assertEqual(self.f_set, f_set)


class TestLinearFuzzySet(unittest.TestCase):
    def setUp(self):
        self.f_set = linear_fuzzy_set.LinearFuzzySet(1, 10)
        self.f_set.add_point(Point(1, 0))
        self.f_set.add_point(Point(2, 0))
        self.f_set.add_point(Point(4, 1))
        self.f_set.add_point(Point(6, 1))
        self.f_set.add_point(Point(8, 0))
        self.f_set.add_point(Point(10, 0))

    def test_belongs_degree(self):
        self.assertEqual(self.f_set.belongs_value(-1), 0)
        self.assertEqual(self.f_set.belongs_value(11), 0)
        self.assertEqual(self.f_set.belongs_value(1), 0)
        self.assertEqual(self.f_set.belongs_value(4), 1)
        self.assertEqual(self.f_set.belongs_value(5), 1)
        self.assertEqual(self.f_set.belongs_value(7), .5)
        self.assertEqual(self.f_set.belongs_value(9), 0)

    def test_merge(self):
        f_set = linear_fuzzy_set.LinearFuzzySet(5, 15)
        f_set.add_point(Point(5, 0))
        f_set.add_point(Point(7, 0))
        f_set.add_point(Point(9, 1))
        f_set.add_point(Point(11, 1))
        f_set.add_point(Point(13, 0))
        f_set.add_point(Point(15, 0))

        f_excepted = linear_fuzzy_set.LinearFuzzySet(1, 15)
        f_excepted.add_point(Point(1, 0))
        f_excepted.add_point(Point(2, 0))
        f_excepted.add_point(Point(4, 1))
        f_excepted.add_point(Point(6, 1))
        f_excepted.add_point(Point(7.5, .25))
        f_excepted.add_point(Point(9, 1))
        f_excepted.add_point(Point(11, 1))
        f_excepted.add_point(Point(13, 0))
        f_excepted.add_point(Point(15, 0))

        self.fuzzy_test_equals(f_set | self.f_set, f_excepted)

        f_excepted = linear_fuzzy_set.LinearFuzzySet(1, 15)
        f_excepted.add_point(Point(1, 0))
        f_excepted.add_point(Point(7, 0))
        f_excepted.add_point(Point(7.5, .25))
        f_excepted.add_point(Point(8, 0))
        f_excepted.add_point(Point(15, 0))

        self.fuzzy_test_equals(self.f_set & f_set, f_excepted)

    def test_merge_2(self):
        f_set = linear_fuzzy_set.LinearFuzzySet(0, 8)
        f_set.add_point_from_coord(0, 0)
        f_set.add_point_from_coord(2, 1)
        f_set.add_point_from_coord(4, 1)
        f_set.add_point_from_coord(5, 0)
        f_set.add_point_from_coord(6, 0)
        f_set.add_point_from_coord(6.5, 1)
        f_set.add_point_from_coord(8, 0)

        f_set2 = linear_fuzzy_set.LinearFuzzySet(2, 7)
        f_set2.add_point_from_coord(2, .5)
        f_set2.add_point_from_coord(3, .5)
        f_set2.add_point_from_coord(4, 0)
        f_set2.add_point_from_coord(5, 1)
        f_set2.add_point_from_coord(6, 1)
        f_set2.add_point_from_coord(7, .5)

        f_excepted = linear_fuzzy_set.LinearFuzzySet(0, 8)
        f_excepted.add_point_from_coord(0, .5)
        f_excepted.add_point_from_coord(1, .5)
        f_excepted.add_point_from_coord(2, 1)
        f_excepted.add_point_from_coord(4, 1)
        f_excepted.add_point_from_coord(4.5, .5)
        f_excepted.add_point_from_coord(5, 1)
        f_excepted.add_point_from_coord(6, 1)
        f_excepted.add_point_from_coord(6.4, .8)
        f_excepted.add_point_from_coord(6.5, 1)
        f_excepted.add_point_from_coord(7.25, .5)
        f_excepted.add_point_from_coord(8, .5)

        self.fuzzy_test_equals(f_set | f_set2, f_excepted)

        f_excepted = linear_fuzzy_set.LinearFuzzySet(0, 8)
        f_excepted.add_point_from_coord(0, 0)
        f_excepted.add_point_from_coord(1.0, 0.5)
        f_excepted.add_point_from_coord(3, 0.5)
        f_excepted.add_point_from_coord(4, 0)
        f_excepted.add_point_from_coord(4.5, 0.5)
        f_excepted.add_point_from_coord(5, 0)
        f_excepted.add_point_from_coord(6, 0)
        f_excepted.add_point_from_coord(6.5, 0.75)
        f_excepted.add_point_from_coord(7, 0.5)
        f_excepted.add_point_from_coord(7.25, 0.5)
        f_excepted.add_point_from_coord(8, 0)

        self.fuzzy_test_equals(f_set & f_set2, f_excepted)

    def test_barycenter(self):
        self.assertAlmostEqual(self.f_set.barycenter(), 5.)

        f_set = linear_fuzzy_set.LinearFuzzySet(0, 11)
        f_set.add_point_from_coord(0, 0)
        f_set.add_point_from_coord(6, 1)
        f_set.add_point_from_coord(8, 1)
        f_set.add_point_from_coord(11, 0)

        self.assertAlmostEqual(f_set.barycenter(), 6.0769230769231)

        f_set = linear_fuzzy_set.LinearFuzzySet(0, 5)
        f_set.add_point_from_coord(0, 0)
        f_set.add_point_from_coord(2, .5)
        f_set.add_point_from_coord(3, 1)
        f_set.add_point_from_coord(5, 0)

        self.assertAlmostEqual(f_set.barycenter(), 2.7777777777778)

        f_set = linear_fuzzy_set.LinearFuzzySet(0, 5)
        f_set.add_point_from_coord(0, .5)
        f_set.add_point_from_coord(2, 1)
        f_set.add_point_from_coord(4, .5)
        f_set.add_point_from_coord(5, 0)

        self.assertAlmostEqual(f_set.barycenter(), 2.1794871794872)

    def fuzzy_test_equals(self, set1: fuzzy_set.BaseFuzzySet, set2: fuzzy_set.BaseFuzzySet):
        self.assertEqual(set1.min, set2.min, "Fuzzy sets are different")
        self.assertEqual(set1.max, set2.max, "Fuzzy sets are different")
        for p1, p2 in zip_longest(set1.points, set2.points):
            self.assertIsNotNone(p1, "Fuzzy sets are different")
            self.assertIsNotNone(p2, "Fuzzy sets are different")
            self.assertAlmostEqual(p1.x, p2.x, None, "Fuzzy sets are different")
            self.assertAlmostEqual(p1.y, p2.y, None, "Fuzzy sets are different")


class TestFuzzySetLinearHelpers(unittest.TestCase):

    def test_left_trapeze_set(self):
        s = linear_fuzzy_set_helpers.left_trapeze_set(0, 10, 4, 6)
        s_excepted = linear_fuzzy_set.LinearFuzzySet(0, 10)
        s_excepted.add_point_from_coord(0, 1)
        s_excepted.add_point_from_coord(4, 1)
        s_excepted.add_point_from_coord(6, 0)
        s_excepted.add_point_from_coord(10, 0)

        self.assertEqual(s, s_excepted)

    def test_right_trapeze_set(self):
        s = linear_fuzzy_set_helpers.right_trapeze_set(0, 10, 4, 6)
        s_excepted = linear_fuzzy_set.LinearFuzzySet(0, 10)
        s_excepted.add_point_from_coord(0, 0)
        s_excepted.add_point_from_coord(4, 0)
        s_excepted.add_point_from_coord(6, 1)
        s_excepted.add_point_from_coord(10, 1)

        self.assertEqual(s, s_excepted)

    def test_trapeze_set(self):
        s = linear_fuzzy_set_helpers.trapeze_set(0, 10, 3, 4, 5, 6)
        s_excepted = linear_fuzzy_set.LinearFuzzySet(0, 10)
        s_excepted.add_point_from_coord(0, 0)
        s_excepted.add_point_from_coord(3, 0)
        s_excepted.add_point_from_coord(4, 1)
        s_excepted.add_point_from_coord(5, 1)
        s_excepted.add_point_from_coord(6, 0)
        s_excepted.add_point_from_coord(10, 0)

        self.assertEqual(s, s_excepted)

    def test_triangle_set(self):
        s = linear_fuzzy_set_helpers.triangle_set(0, 10, 4, 5, 7)
        s_excepted = linear_fuzzy_set.LinearFuzzySet(0, 10)
        s_excepted.add_point_from_coord(0, 0)
        s_excepted.add_point_from_coord(4, 0)
        s_excepted.add_point_from_coord(5, 1)
        s_excepted.add_point_from_coord(7, 0)
        s_excepted.add_point_from_coord(10, 0)

        self.assertEqual(s, s_excepted)

    def test_constant_set(self):
        s = linear_fuzzy_set_helpers.constant_set(0, 1, .3)
        s_excepted = linear_fuzzy_set.LinearFuzzySet(0, 1)
        s_excepted.add_point_from_coord(0, .3)
        s_excepted.add_point_from_coord(1, .3)

        self.assertEqual(s, s_excepted)


if __name__ == '__main__':
    unittest.main()
