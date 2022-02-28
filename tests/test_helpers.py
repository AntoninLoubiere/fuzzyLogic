import unittest
import helpers


class TestHelpers(unittest.TestCase):
    def test_signum(self):
        self.assertEqual(helpers.signum(0), 0)
        self.assertEqual(helpers.signum(0.1), 1)
        self.assertEqual(helpers.signum(10), 1)
        self.assertEqual(helpers.signum(-0.1), -1)
        self.assertEqual(helpers.signum(-10), -1)


if __name__ == '__main__':
    unittest.main()
