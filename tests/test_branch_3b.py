# Тесты Ветви 3b. Разбор выражений: парсер и вычислитель.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_3b_parser import (
    current_token, apply_binary, power_signed,
    parse_factor, parse_power, parse_term, parse_expression, calculate,
)


class TestCurrentToken(unittest.TestCase):
    def test_existing(self):
        self.assertEqual(current_token([("number", 1)], 0), ("number", 1))

    def test_beyond_end(self):
        self.assertEqual(current_token([], 0), ("end", None))


class TestApplyBinary(unittest.TestCase):
    def test_all_operations(self):
        self.assertEqual(apply_binary("+", 1, 2), 3)
        self.assertEqual(apply_binary("-", 5, 2), 3)
        self.assertEqual(apply_binary("*", 3, 4), 12)
        self.assertAlmostEqual(apply_binary("/", 7, 2), 3.5)
        self.assertEqual(apply_binary("%", 7, 3), 1)
        self.assertEqual(apply_binary("^", 2, 10), 1024)

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            apply_binary("&", 1, 2)


class TestPowerSigned(unittest.TestCase):
    def test_zero_power(self):
        self.assertEqual(power_signed(5, 0), 1)

    def test_positive(self):
        self.assertEqual(power_signed(2, 3), 8)

    def test_negative(self):
        self.assertAlmostEqual(power_signed(2, -2), 0.25)

    def test_non_integer_rejected(self):
        with self.assertRaises(ValueError):
            power_signed(2, 0.5)


class TestParseFactor(unittest.TestCase):
    def test_number(self):
        self.assertEqual(parse_factor([("number", 7)], 0), (7, 1))

    def test_unary_minus(self):
        tokens = [("operator", "-"), ("number", 5)]
        self.assertEqual(parse_factor(tokens, 0), (-5, 2))

    def test_unary_plus(self):
        tokens = [("operator", "+"), ("number", 5)]
        self.assertEqual(parse_factor(tokens, 0), (5, 2))

    def test_parentheses(self):
        tokens = [("left_paren", "("), ("number", 4), ("right_paren", ")")]
        self.assertEqual(parse_factor(tokens, 0), (4, 3))

    def test_missing_closing_paren(self):
        tokens = [("left_paren", "("), ("number", 4)]
        with self.assertRaises(ValueError):
            parse_factor(tokens, 0)


class TestParsePower(unittest.TestCase):
    def test_right_associativity(self):
        # 2 ^ 3 ^ 2 = 2 ^ 9 = 512
        tokens = [("number", 2), ("operator", "^"), ("number", 3),
                  ("operator", "^"), ("number", 2)]
        self.assertEqual(parse_power(tokens, 0), (512, 5))

    def test_single_number(self):
        self.assertEqual(parse_power([("number", 9)], 0), (9, 1))


class TestParseTerm(unittest.TestCase):
    def test_multiplication_chain(self):
        # 2 * 3 * 4 = 24
        tokens = [("number", 2), ("operator", "*"), ("number", 3),
                  ("operator", "*"), ("number", 4)]
        self.assertEqual(parse_term(tokens, 0), (24, 5))


class TestParseExpression(unittest.TestCase):
    def test_addition_chain(self):
        # 1 + 2 + 3 = 6
        tokens = [("number", 1), ("operator", "+"), ("number", 2),
                  ("operator", "+"), ("number", 3)]
        self.assertEqual(parse_expression(tokens, 0), (6, 5))


class TestCalculate(unittest.TestCase):
    def test_priority(self):
        self.assertEqual(calculate("2 + 2 * 2"), 6)

    def test_simple(self):
        self.assertEqual(calculate("2+2"), 4)

    def test_spaces(self):
        self.assertEqual(calculate("  10 - 4 "), 6)

    def test_float(self):
        self.assertAlmostEqual(calculate("1.5 * 2"), 3.0)

    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 2) * 2"), 8)

    def test_nested_parentheses(self):
        self.assertEqual(calculate("((1 + 2) * (3 + 4))"), 21)

    def test_unary_minus(self):
        self.assertEqual(calculate("-5 + 10"), 5)

    def test_double_unary_minus(self):
        self.assertEqual(calculate("--5"), 5)

    def test_unary_plus(self):
        self.assertEqual(calculate("+5 + 3"), 8)

    def test_unary_minus_with_power(self):
        # -2 ^ 2 = -(2 ^ 2) = -4
        self.assertEqual(calculate("-2 ^ 2"), -4)

    def test_power_right_associative(self):
        self.assertEqual(calculate("2 ^ 3 ^ 2"), 512)

    def test_negative_power(self):
        self.assertAlmostEqual(calculate("2 ^ -2"), 0.25)

    def test_remainder(self):
        self.assertEqual(calculate("7 % 3"), 1)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate("1 / 0")

    def test_trailing_operator(self):
        with self.assertRaises(ValueError):
            calculate("2 +")

    def test_extra_closing_paren(self):
        with self.assertRaises(ValueError):
            calculate("2 + 2)")

    def test_missing_closing_paren(self):
        with self.assertRaises(ValueError):
            calculate("(2 + 2")

    def test_two_numbers(self):
        with self.assertRaises(ValueError):
            calculate("2 2")

    def test_empty(self):
        with self.assertRaises(ValueError):
            calculate("")

    def test_invalid_symbol(self):
        with self.assertRaises(ValueError):
            calculate("2 # 3")


if __name__ == "__main__":
    unittest.main()
