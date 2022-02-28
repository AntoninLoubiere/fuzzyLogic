import unittest
import points


class TestPoints(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.point1 = points.Point(40, 0)
        self.point2 = points.Point(82, 1)
        self.point3 = points.Point(75, .5)

    def test_randoms_points(self):
        self.assertEqual(self.point1.x, 40)
        self.assertEqual(self.point1.y, 0)

        self.assertEqual(self.point2.x, 82)
        self.assertEqual(self.point2.y, 1)

        self.assertEqual(self.point3.x, 75)
        self.assertEqual(self.point3.y, .5)

    def test_comparisons(self):
        self.assertTrue(self.point1 < self.point2)
        self.assertTrue(self.point1 < self.point3)
        self.assertTrue(self.point2 > self.point3)
        self.assertTrue(self.point1 != self.point3)
        self.assertFalse(self.point2 == self.point3)

    def test_not_operator(self):
        self.assertEqual(self.point1.not_operator(), points.Point(40, 1))
        self.assertEqual(self.point2.not_operator(), points.Point(82, 0))
        self.assertEqual(self.point3.not_operator(), points.Point(75, .5))

    def test_multiply_points(self):
        point = self.point1 * .2
        self.assertEqual(point.x, 40)
        self.assertEqual(point.y, 0)

        point = self.point2 * .2
        self.assertEqual(point.x, 82)
        self.assertEqual(point.y, .2)

        point = self.point3 * .6
        self.assertEqual(point.x, 75)
        self.assertEqual(point.y, .3)

        self.test_randoms_points()  # verify that the points haven't change

    def test_i_multiply_points(self):
        self.point1 *= .2
        self.assertEqual(self.point1.x, 40)
        self.assertEqual(self.point1.y, 0)

        self.point2 *= .2
        self.assertEqual(self.point2.x, 82)
        self.assertEqual(self.point2.y, .2)

        self.point3 *= .6
        self.assertEqual(self.point3.x, 75)
        self.assertEqual(self.point3.y, .3)


if __name__ == '__main__':
    unittest.main()
