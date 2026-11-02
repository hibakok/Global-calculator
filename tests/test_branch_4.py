# Тесты Ветви 4. Научные функции.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_4_scientific import abs_value, sign


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


if __name__ == "__main__":
    unittest.main()
