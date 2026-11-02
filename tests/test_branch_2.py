# Тесты Ветви 2. Расширенная арифметика.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_2_extended import power_int, int_divide, remainder, percent, root_int


class TestPowerInt(unittest.TestCase):
    def test_zero_power(self):
        self.assertEqual(power_int(5, 0), 1)

    def test_positive_power(self):
        self.assertEqual(power_int(2, 10), 1024)

    def test_negative_base(self):
        self.assertEqual(power_int(-2, 3), -8)

    def test_float_base(self):
        self.assertAlmostEqual(power_int(1.5, 2), 2.25)

    def test_negative_power_rejected(self):
        with self.assertRaises(ValueError):
            power_int(2, -1)


class TestIntDivide(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(int_divide(7, 2), 3)

    def test_negative_dividend(self):
        self.assertEqual(int_divide(-7, 2), -4)

    def test_exact(self):
        self.assertEqual(int_divide(9, 3), 3)

    def test_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):
            int_divide(5, 0)


class TestRemainder(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(remainder(7, 2), 1)

    def test_negative_dividend(self):
        self.assertEqual(remainder(-7, 2), 1)

    def test_exact(self):
        self.assertEqual(remainder(9, 3), 0)

    def test_zero_divisor(self):
        with self.assertRaises(ZeroDivisionError):
            remainder(5, 0)


class TestPercent(unittest.TestCase):
    def test_simple(self):
        self.assertAlmostEqual(percent(200, 10), 20.0)

    def test_more_than_hundred(self):
        self.assertAlmostEqual(percent(50, 200), 100.0)

    def test_zero_value(self):
        self.assertAlmostEqual(percent(0, 25), 0.0)

class TestRootInt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(root_int(0, 2), 0)

    def test_one(self):
        self.assertEqual(root_int(1, 2), 1)

    def test_exact_cube(self):
        self.assertEqual(root_int(8, 3), 2)

    def test_not_exact(self):
        self.assertEqual(root_int(10, 3), 2)

    def test_exact_square(self):
        self.assertEqual(root_int(9, 2), 3)

    def test_big_number(self):
        self.assertEqual(root_int(10 ** 18, 2), 10 ** 9)

    def test_first_power(self):
        self.assertEqual(root_int(7, 1), 7)

    def test_negative_value_rejected(self):
        with self.assertRaises(ValueError):
            root_int(-4, 2)

    def test_zero_power_rejected(self):
        with self.assertRaises(ValueError):
            root_int(5, 0)


if __name__ == "__main__":
    unittest.main()
