# Тесты Ветви 6b. Научные выражения: таблицы имён, операции и парсер.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_6b_scientific_parser import (
    apply_scientific, is_constant, constant_value, is_function,
    apply_function, parse_call, parse_factor_scientific,
    parse_power_scientific, parse_term_scientific,
    parse_expression_scientific, calculate_scientific,
)
from branch_6a_scientific_tokenizer import tokenize_scientific


class TestApplyScientific(unittest.TestCase):
    def test_plus(self):
        self.assertEqual(apply_scientific("+", 2, 3), 5)

    def test_divide(self):
        self.assertEqual(apply_scientific("/", 7, 2), 3.5)

    def test_power_int(self):
        self.assertEqual(apply_scientific("^", 2, 10), 1024)

    def test_power_real(self):
        self.assertAlmostEqual(apply_scientific("^", 2, 0.5), 1.4142135623730951)

    def test_negative_base_integer_power(self):
        self.assertEqual(apply_scientific("^", -2, 3), -8)

    def test_negative_base_real_power(self):
        with self.assertRaises(ValueError):
            apply_scientific("^", -2, 0.5)

    def test_zero_base_negative_power(self):
        with self.assertRaises(ZeroDivisionError):
            apply_scientific("^", 0, -1)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            apply_scientific("/", 1, 0)

    def test_unknown_operation(self):
        with self.assertRaises(ValueError):
            apply_scientific("&", 1, 2)


class TestIsConstant(unittest.TestCase):
    def test_pi(self):
        self.assertTrue(is_constant("pi"))

    def test_e(self):
        self.assertTrue(is_constant("e"))

    def test_function_name(self):
        self.assertFalse(is_constant("sqrt"))

    def test_unknown(self):
        self.assertFalse(is_constant("x"))


class TestConstantValue(unittest.TestCase):
    def test_pi(self):
        self.assertAlmostEqual(constant_value("pi"), 3.141592653589793)

    def test_e(self):
        self.assertAlmostEqual(constant_value("e"), 2.718281828459045)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            constant_value("tau")


class TestIsFunction(unittest.TestCase):
    def test_sqrt(self):
        self.assertTrue(is_function("sqrt"))

    def test_tan(self):
        self.assertTrue(is_function("tan"))

    def test_constant_name(self):
        self.assertFalse(is_function("pi"))

    def test_unknown(self):
        self.assertFalse(is_function("sqr"))


class TestApplyFunction(unittest.TestCase):
    def test_sqrt(self):
        self.assertAlmostEqual(apply_function("sqrt", 9), 3)

    def test_exp(self):
        self.assertAlmostEqual(apply_function("exp", 1), 2.718281828459045)

    def test_ln(self):
        self.assertAlmostEqual(apply_function("ln", 2.718281828459045), 1)

    def test_sin(self):
        self.assertAlmostEqual(apply_function("sin", 1.5707963267948966), 1)

    def test_cos(self):
        self.assertAlmostEqual(apply_function("cos", 0), 1)

    def test_tan(self):
        self.assertAlmostEqual(apply_function("tan", 0), 0)

    def test_sqrt_negative(self):
        with self.assertRaises(ValueError):
            apply_function("sqrt", -1)

    def test_ln_non_positive(self):
        with self.assertRaises(ValueError):
            apply_function("ln", 0)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            apply_function("log", 10)


class TestParseCall(unittest.TestCase):
    def test_call(self):
        tokens = tokenize_scientific("sqrt(9)")
        value, pos = parse_call(tokens, 0)
        self.assertAlmostEqual(value, 3)
        self.assertEqual(pos, 4)

    def test_nested_expression(self):
        tokens = tokenize_scientific("sin(pi / 2)")
        value, pos = parse_call(tokens, 0)
        self.assertAlmostEqual(value, 1)
        self.assertEqual(pos, 6)

    def test_missing_opening_paren(self):
        tokens = tokenize_scientific("sqrt 2")
        with self.assertRaises(ValueError):
            parse_call(tokens, 0)

    def test_missing_closing_paren(self):
        tokens = tokenize_scientific("sqrt(2")
        with self.assertRaises(ValueError):
            parse_call(tokens, 0)


class TestParseFactorScientific(unittest.TestCase):
    def test_number(self):
        tokens = tokenize_scientific("42")
        self.assertEqual(parse_factor_scientific(tokens, 0), (42, 1))

    def test_constant(self):
        tokens = tokenize_scientific("pi")
        value, pos = parse_factor_scientific(tokens, 0)
        self.assertAlmostEqual(value, 3.141592653589793)
        self.assertEqual(pos, 1)

    def test_function_call(self):
        tokens = tokenize_scientific("sqrt(4)")
        value, pos = parse_factor_scientific(tokens, 0)
        self.assertAlmostEqual(value, 2)
        self.assertEqual(pos, 4)

    def test_unary_minus(self):
        tokens = tokenize_scientific("-5")
        self.assertEqual(parse_factor_scientific(tokens, 0), (-5, 2))

    def test_unary_plus(self):
        tokens = tokenize_scientific("+5")
        self.assertEqual(parse_factor_scientific(tokens, 0), (5, 2))

    def test_parentheses(self):
        tokens = tokenize_scientific("(1 + 2)")
        self.assertEqual(parse_factor_scientific(tokens, 0), (3, 5))

    def test_unknown_name(self):
        tokens = tokenize_scientific("foo")
        with self.assertRaises(ValueError):
            parse_factor_scientific(tokens, 0)

    def test_end_of_tokens(self):
        with self.assertRaises(ValueError):
            parse_factor_scientific([], 0)


class TestParsePowerScientific(unittest.TestCase):
    def test_simple(self):
        tokens = tokenize_scientific("2 ^ 3")
        self.assertEqual(parse_power_scientific(tokens, 0), (8, 3))

    def test_right_associative(self):
        tokens = tokenize_scientific("2 ^ 3 ^ 2")
        self.assertEqual(parse_power_scientific(tokens, 0), (512, 5))

    def test_real_exponent(self):
        tokens = tokenize_scientific("2 ^ 0.5")
        value, pos = parse_power_scientific(tokens, 0)
        self.assertAlmostEqual(value, 1.4142135623730951)
        self.assertEqual(pos, 3)

    def test_without_power(self):
        tokens = tokenize_scientific("2 + 3")
        self.assertEqual(parse_power_scientific(tokens, 0), (2, 1))


class TestParseTermScientific(unittest.TestCase):
    def test_chain(self):
        tokens = tokenize_scientific("2 * 3 % 4")
        self.assertEqual(parse_term_scientific(tokens, 0), (2, 5))

    def test_left_associative_division(self):
        tokens = tokenize_scientific("8 / 4 / 2")
        self.assertEqual(parse_term_scientific(tokens, 0), (1.0, 5))

    def test_stops_at_plus(self):
        tokens = tokenize_scientific("2 * 3 + 4")
        self.assertEqual(parse_term_scientific(tokens, 0), (6, 3))


class TestParseExpressionScientific(unittest.TestCase):
    def test_chain(self):
        tokens = tokenize_scientific("1 + 2 - 3")
        self.assertEqual(parse_expression_scientific(tokens, 0), (0, 5))

    def test_priority_of_term(self):
        tokens = tokenize_scientific("2 * 3 + 4")
        self.assertEqual(parse_expression_scientific(tokens, 0), (10, 5))


class TestCalculateScientific(unittest.TestCase):
    def test_roadmap_example(self):
        self.assertAlmostEqual(
            calculate_scientific("sqrt(2) + sin(pi/2)"), 2.414213562373095)

    def test_priority(self):
        self.assertEqual(calculate_scientific("1 + 2 * 3"), 7)

    def test_parentheses(self):
        self.assertEqual(calculate_scientific("(1 + 2) * 3"), 9)

    def test_power_real(self):
        self.assertAlmostEqual(calculate_scientific("2 ^ 0.5"),
                               1.4142135623730951)

    def test_power_right_associative(self):
        self.assertEqual(calculate_scientific("2 ^ 3 ^ 2"), 512)

    def test_unary_minus_binds_less_than_power(self):
        self.assertEqual(calculate_scientific("-2 ^ 2"), -4)

    def test_negative_exponent(self):
        self.assertEqual(calculate_scientific("2 ^ -2"), 0.25)

    def test_exponent_number(self):
        self.assertEqual(calculate_scientific("2e3 + 1"), 2001.0)

    def test_constant_e_power(self):
        self.assertAlmostEqual(calculate_scientific("e ^ 2"),
                               7.38905609893065)

    def test_ln_of_e(self):
        self.assertAlmostEqual(calculate_scientific("ln(e)"), 1)

    def test_cos_zero(self):
        self.assertAlmostEqual(calculate_scientific("cos(0)"), 1)

    def test_tan_zero(self):
        self.assertAlmostEqual(calculate_scientific("tan(0)"), 0)

    def test_remainder(self):
        self.assertEqual(calculate_scientific("10 % 3"), 1)

    def test_spaces(self):
        self.assertEqual(calculate_scientific("  1   +   1 "), 2)

    def test_empty(self):
        with self.assertRaises(ValueError):
            calculate_scientific("")

    def test_spaces_only(self):
        with self.assertRaises(ValueError):
            calculate_scientific("   ")

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            calculate_scientific("2 + foo")

    def test_not_fully_parsed(self):
        with self.assertRaises(ValueError):
            calculate_scientific("2 2")

    def test_negative_base_real_power(self):
        with self.assertRaises(ValueError):
            calculate_scientific("(-2) ^ 0.5")

    def test_sqrt_of_negative(self):
        with self.assertRaises(ValueError):
            calculate_scientific("sqrt(-1)")

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_scientific("1 / 0")

    def test_function_without_parentheses(self):
        with self.assertRaises(ValueError):
            calculate_scientific("sqrt 2")


if __name__ == "__main__":
    unittest.main()