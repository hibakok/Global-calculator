# Тесты Ветви 5. Тригонометрия.
# Запуск из корня репозитория: python -m unittest discover -s tests -v
# Модуль math используется только как эталон для сравнения:
# в src всё вычисляется собственными рядами.

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_5_trigonometry import (
    arctan_series, get_pi, reduce_angle, sin_series, cos_series,
    sin_rad, cos_rad, tan_rad,
)


class TestArctanSeries(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(arctan_series(0), 0)

    def test_fifth(self):
        self.assertAlmostEqual(arctan_series(0.2), math.atan(0.2), places=14)

    def test_one_over_239(self):
        self.assertAlmostEqual(arctan_series(1 / 239), math.atan(1 / 239), places=14)

    def test_half(self):
        self.assertAlmostEqual(arctan_series(0.5), math.atan(0.5), places=13)
        self.assertAlmostEqual(arctan_series(-0.5), math.atan(-0.5), places=13)

    def test_boundaries_rejected(self):
        with self.assertRaises(ValueError):
            arctan_series(1)
        with self.assertRaises(ValueError):
            arctan_series(-1)

    def test_nan_returns_nan(self):
        result = arctan_series(float("nan"))
        self.assertNotEqual(result, result)


class TestGetPi(unittest.TestCase):
    def test_value(self):
        self.assertAlmostEqual(get_pi(), 3.141592653589793, delta=1e-14)

    def test_matches_math(self):
        self.assertAlmostEqual(get_pi(), math.pi, delta=1e-14)

    def test_is_float(self):
        self.assertIsInstance(get_pi(), float)


class TestReduceAngle(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(reduce_angle(0), (0, 0.0))

    def test_pi(self):
        k, r = reduce_angle(get_pi())
        self.assertEqual(k, 1)
        self.assertEqual(r, 0.0)

    def test_two_pi(self):
        k, r = reduce_angle(2 * get_pi())
        self.assertEqual(k, 2)
        self.assertEqual(r, 0.0)

    def test_half_pi(self):
        k, r = reduce_angle(get_pi() / 2)
        self.assertEqual(k, 0)
        self.assertAlmostEqual(r, get_pi() / 2, places=15)

    def test_negative_angle(self):
        k, r = reduce_angle(-10.5)
        self.assertEqual(k, -3)
        self.assertLessEqual(abs(r), get_pi() / 2 + 1e-12)

    def test_nan_returns_nan(self):
        k, r = reduce_angle(float("nan"))
        self.assertNotEqual(r, r)

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            reduce_angle(float("inf"))
        with self.assertRaises(ValueError):
            reduce_angle(float("-inf"))


class TestSinSeries(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(sin_series(0), 0)

    def test_one(self):
        self.assertAlmostEqual(sin_series(1), math.sin(1), places=14)

    def test_minus_one(self):
        self.assertAlmostEqual(sin_series(-1), math.sin(-1), places=14)

    def test_half_pi(self):
        self.assertAlmostEqual(sin_series(get_pi() / 2), 1, delta=1e-14)

    def test_nan_returns_nan(self):
        result = sin_series(float("nan"))
        self.assertNotEqual(result, result)


class TestCosSeries(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(cos_series(0), 1.0)

    def test_one(self):
        self.assertAlmostEqual(cos_series(1), math.cos(1), places=14)

    def test_minus_one(self):
        self.assertAlmostEqual(cos_series(-1), math.cos(1), places=14)

    def test_half_pi(self):
        # Вблизи pi/2 косинус почти нулевой: сравниваем с эталоном в той же
        # точке с допуском на сокращение членов ряда.
        self.assertAlmostEqual(cos_series(get_pi() / 2), math.cos(get_pi() / 2),
                               delta=1e-15)

    def test_nan_returns_nan(self):
        result = cos_series(float("nan"))
        self.assertNotEqual(result, result)


class TestSinRad(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(sin_rad(0), 0)

    def test_half_pi(self):
        self.assertAlmostEqual(sin_rad(get_pi() / 2), 1, delta=1e-14)

    def test_pi_is_exact_zero(self):
        self.assertEqual(sin_rad(get_pi()), 0)

    def test_two_pi(self):
        self.assertAlmostEqual(sin_rad(2 * get_pi()), 0, delta=1e-14)

    def test_one(self):
        self.assertAlmostEqual(sin_rad(1), math.sin(1), places=12)

    def test_ten(self):
        self.assertAlmostEqual(sin_rad(10), math.sin(10), places=10)

    def test_negative(self):
        self.assertAlmostEqual(sin_rad(-1), math.sin(-1), places=12)

    def test_nan_returns_nan(self):
        result = sin_rad(float("nan"))
        self.assertNotEqual(result, result)

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            sin_rad(float("inf"))


class TestCosRad(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(cos_rad(0), 1.0)

    def test_pi_is_exact_minus_one(self):
        self.assertEqual(cos_rad(get_pi()), -1.0)

    def test_two_pi(self):
        self.assertEqual(cos_rad(2 * get_pi()), 1.0)

    def test_one(self):
        self.assertAlmostEqual(cos_rad(1), math.cos(1), places=12)

    def test_ten(self):
        self.assertAlmostEqual(cos_rad(10), math.cos(10), places=10)

    def test_nan_returns_nan(self):
        result = cos_rad(float("nan"))
        self.assertNotEqual(result, result)

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            cos_rad(float("inf"))


class TestTanRad(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(tan_rad(0), 0)

    def test_quarter_pi(self):
        self.assertAlmostEqual(tan_rad(get_pi() / 4), 1, delta=1e-12)

    def test_one(self):
        self.assertAlmostEqual(tan_rad(1), math.tan(1), places=10)

    def test_negative(self):
        self.assertAlmostEqual(tan_rad(-1), math.tan(-1), places=10)

    def test_near_pole_is_huge(self):
        # У pi/2 тангенс не определён; рядом с полюсом результат огромен.
        self.assertGreater(abs(tan_rad(get_pi() / 2 - 1e-9)), 1e8)

    def test_nan_returns_nan(self):
        result = tan_rad(float("nan"))
        self.assertNotEqual(result, result)

    def test_infinity_rejected(self):
        with self.assertRaises(ValueError):
            tan_rad(float("inf"))


if __name__ == "__main__":
    unittest.main()