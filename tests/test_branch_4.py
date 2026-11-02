# Тесты Ветви 4. Научные функции.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_4_scientific import abs_value, sign, sqrt_real


class TestAbsValue(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(abs_value(5), 5)

    def test_negative(self):
        self.assertEqual(abs_value(-5), 5)

    def test_zero(self):
        self.assertEqual(abs_value(0), 0)

    def test_negative_float(self):
        self.assertAlmostEqual(abs_value(-2.5), 2.5)


class TestSign(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(sign(7), 1)

    def test_negative(self):
        self.assertEqual(sign(-7), -1)

    def test_zero(self):
        self.assertEqual(sign(0), 0)

    def test_negative_float(self):
        self.assertEqual(sign(-0.5), -1)


class TestSqrtReal(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(sqrt_real(0), 0)

    def test_one(self):
        self.assertEqual(sqrt_real(1), 1)

    def test_perfect_square(self):
        self.assertAlmostEqual(sqrt_real(4), 2)

    def test_two(self):
        self.assertAlmostEqual(sqrt_real(2), 1.4142135623730951)

    def test_fraction(self):
        self.assertAlmostEqual(sqrt_real(0.25), 0.5)

    def test_large(self):
        self.assertAlmostEqual(sqrt_real(1e12), 1e6)

    def test_small(self):
        self.assertAlmostEqual(sqrt_real(1e-8), 1e-4)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            sqrt_real(-4)


if __name__ == "__main__":
    unittest.main()
