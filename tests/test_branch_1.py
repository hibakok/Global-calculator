# Тесты Ветви 1. Элементарная арифметика.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_1_arithmetic import add, subtract, multiply, divide


class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-5, 3), -2)

    def test_float(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestSubtract(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(subtract(7, 3), 4)

    def test_negative_result(self):
        self.assertEqual(subtract(3, 7), -4)

    def test_float(self):
        self.assertAlmostEqual(subtract(1.5, 0.25), 1.25)


class TestMultiply(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(multiply(4, 6), 24)

    def test_negative(self):
        self.assertEqual(multiply(-3, 5), -15)

    def test_zero(self):
        self.assertEqual(multiply(123, 0), 0)

    def test_float(self):
        self.assertAlmostEqual(multiply(2.5, 4.0), 10.0)


class TestDivide(unittest.TestCase):
    def test_even(self):
        self.assertEqual(divide(10, 2), 5.0)

    def test_fraction(self):
        self.assertAlmostEqual(divide(1, 4), 0.25)

    def test_negative(self):
        self.assertAlmostEqual(divide(-9, 3), -3.0)

    def test_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)


if __name__ == "__main__":
    unittest.main()
