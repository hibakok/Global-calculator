# Тесты Ветви 4. Научные функции: экспонента и логарифм.
# Запуск из корня репозитория: python -m unittest discover -s tests -v
# Модуль math используется только как эталон для сравнения:
# в src всё вычисляется собственными рядами и итерациями.

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_4_scientific import (
    abs_value, sign, sqrt_real, exp_series, exp_real, get_e,
    ln_series, get_ln2, ln_positive, power_real,
)


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

    def test_nan_returns_nan_without_hanging(self):
        # nan не должен вызывать вечный цикл: проверка not (nxt < y).
        result = sqrt_real(float("nan"))
        self.assertNotEqual(result, result)


class TestExpSeries(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(exp_series(0), 1.0)

    def test_one(self):
        self.assertAlmostEqual(exp_series(1), math.e, places=14)

    def test_minus_one(self):
        self.assertAlmostEqual(exp_series(-1), 1 / math.e, places=14)

    def test_half(self):
        self.assertAlmostEqual(exp_series(0.5), math.exp(0.5), places=14)

    def test_nan_returns_nan(self):
        result = exp_series(float("nan"))
        self.assertNotEqual(result, result)


class TestExpReal(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(exp_real(0), 1.0)

    def test_one(self):
        self.assertAlmostEqual(exp_real(1), math.e, places=13)

    def test_small_negative(self):
        self.assertAlmostEqual(exp_real(-1), 1 / math.e, places=13)

    def test_moderate(self):
        self.assertAlmostEqual(exp_real(5), math.exp(5), places=12)

    def test_large_positive(self):
        expected = math.exp(50)
        self.assertAlmostEqual(exp_real(50), expected, delta=expected * 1e-11)

    def test_large_negative(self):
        expected = math.exp(-50)
        self.assertAlmostEqual(exp_real(-50), expected, delta=expected * 1e-11)

    def test_very_large(self):
        expected = math.exp(700)
        self.assertAlmostEqual(exp_real(700), expected, delta=expected * 1e-11)

    def test_infinity(self):
        self.assertEqual(exp_real(float("inf")), float("inf"))
        self.assertEqual(exp_real(float("-inf")), 0.0)

    def test_nan_returns_nan(self):
        result = exp_real(float("nan"))
        self.assertNotEqual(result, result)


class TestGetE(unittest.TestCase):
    def test_value(self):
        self.assertAlmostEqual(get_e(), 2.718281828459045, places=14)

    def test_matches_exp_real(self):
        self.assertEqual(get_e(), exp_real(1))

    def test_is_float(self):
        self.assertIsInstance(get_e(), float)


class TestLnSeries(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(ln_series(0), 0)

    def test_positive(self):
        self.assertAlmostEqual(ln_series(0.5), math.log(1.5), places=14)

    def test_negative(self):
        self.assertAlmostEqual(ln_series(-0.5), math.log(0.5), places=14)

    def test_quarter(self):
        self.assertAlmostEqual(ln_series(0.25), math.log(1.25), places=14)

    def test_boundary_values_rejected(self):
        with self.assertRaises(ValueError):
            ln_series(1)
        with self.assertRaises(ValueError):
            ln_series(-1)

    def test_nan_returns_nan(self):
        result = ln_series(float("nan"))
        self.assertNotEqual(result, result)


class TestGetLn2(unittest.TestCase):
    def test_value(self):
        self.assertAlmostEqual(get_ln2(), 0.6931471805599453, places=14)

    def test_matches_math(self):
        self.assertAlmostEqual(get_ln2(), math.log(2), places=14)


class TestLnPositive(unittest.TestCase):
    def test_one(self):
        self.assertEqual(ln_positive(1), 0)

    def test_two(self):
        self.assertAlmostEqual(ln_positive(2), math.log(2), places=13)

    def test_e_gives_one(self):
        self.assertAlmostEqual(ln_positive(get_e()), 1, places=12)

    def test_half(self):
        self.assertAlmostEqual(ln_positive(0.5), math.log(0.5), places=13)

    def test_huge(self):
        expected = math.log(1e100)
        self.assertAlmostEqual(ln_positive(1e100), expected, delta=abs(expected) * 1e-13)

    def test_tiny(self):
        expected = math.log(1e-100)
        self.assertAlmostEqual(ln_positive(1e-100), expected, delta=abs(expected) * 1e-13)

    def test_infinity(self):
        self.assertEqual(ln_positive(float("inf")), float("inf"))

    def test_zero_and_negative_rejected(self):
        with self.assertRaises(ValueError):
            ln_positive(0)
        with self.assertRaises(ValueError):
            ln_positive(-5)

    def test_nan_returns_nan(self):
        result = ln_positive(float("nan"))
        self.assertNotEqual(result, result)


class TestPowerReal(unittest.TestCase):
    def test_integer_power_exact(self):
        self.assertEqual(power_real(2, 10), 1024)

    def test_negative_integer_power(self):
        self.assertAlmostEqual(power_real(2, -2), 0.25)

    def test_float_integer_power(self):
        self.assertEqual(power_real(2.0, 2.0), 4.0)

    def test_half_power(self):
        self.assertAlmostEqual(power_real(4, 0.5), 2, places=12)

    def test_sqrt_of_two(self):
        self.assertAlmostEqual(power_real(2, 0.5), math.sqrt(2), places=12)

    def test_negative_base_integer_power(self):
        self.assertEqual(power_real(-8, 3), -512)
        self.assertAlmostEqual(power_real(-2, -3), -0.125)

    def test_zero_base(self):
        self.assertEqual(power_real(0, 0), 1)
        self.assertEqual(power_real(0, 0.5), 0.0)

    def test_zero_negative_power_rejected(self):
        with self.assertRaises(ZeroDivisionError):
            power_real(0, -1)
        with self.assertRaises(ZeroDivisionError):
            power_real(0, -0.5)

    def test_negative_base_fractional_rejected(self):
        with self.assertRaises(ValueError):
            power_real(-8, 0.5)

    def test_nan_returns_nan(self):
        result = power_real(2, float("nan"))
        self.assertNotEqual(result, result)
        result = power_real(float("nan"), 2)
        self.assertNotEqual(result, result)


if __name__ == "__main__":
    unittest.main()