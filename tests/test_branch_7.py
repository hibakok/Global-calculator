# Тесты Ветви 7. Память и история: переменные, ans, стек и журнал.
# Запуск из корня репозитория: python -m unittest discover -s tests -v

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch_7_memory import (
    make_memory, find_equals, is_valid_name, split_assignment,
    is_reserved_name, substitute_token, substitute_variables,
    evaluate_tokens, assign_variable, calculate_with_memory,
    make_session, remember_answer, push_result, log_operation,
    remember_result, get_answer, get_results, get_log,
    calculate_session,
)
from branch_6a_scientific_tokenizer import tokenize_scientific


class TestMakeMemory(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(make_memory(), {})

    def test_independent(self):
        first = make_memory()
        second = make_memory()
        first["x"] = 1
        self.assertEqual(second, {})


class TestFindEquals(unittest.TestCase):
    def test_found(self):
        self.assertEqual(find_equals("x = 2"), 2)

    def test_not_found(self):
        self.assertEqual(find_equals("2 + 2"), -1)

    def test_first_of_several(self):
        self.assertEqual(find_equals("a = b = 1"), 2)


class TestIsValidName(unittest.TestCase):
    def test_single_letter(self):
        self.assertTrue(is_valid_name("x"))

    def test_word(self):
        self.assertTrue(is_valid_name("speed"))

    def test_uppercase(self):
        self.assertTrue(is_valid_name("X"))

    def test_empty(self):
        self.assertFalse(is_valid_name(""))

    def test_with_digit(self):
        self.assertFalse(is_valid_name("x1"))

    def test_with_space(self):
        self.assertFalse(is_valid_name("x y"))


class TestSplitAssignment(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(split_assignment("x = 2 + 2"), ("x", "2 + 2"))

    def test_no_spaces(self):
        self.assertEqual(split_assignment("y=1"), ("y", "1"))

    def test_spaces_around_name(self):
        self.assertEqual(split_assignment("  x  =  5 "), ("x", "5"))

    def test_no_equals(self):
        self.assertIsNone(split_assignment("2 + 2"))

    def test_expression_on_left(self):
        with self.assertRaises(ValueError):
            split_assignment("2 + 2 = x")

    def test_two_names_on_left(self):
        with self.assertRaises(ValueError):
            split_assignment("x y = 1")


class TestIsReservedName(unittest.TestCase):
    def test_constant_pi(self):
        self.assertTrue(is_reserved_name("pi"))

    def test_constant_e(self):
        self.assertTrue(is_reserved_name("e"))

    def test_function_sin(self):
        self.assertTrue(is_reserved_name("sin"))

    def test_variable_name(self):
        self.assertFalse(is_reserved_name("x"))


class TestSubstituteToken(unittest.TestCase):
    def test_variable(self):
        self.assertEqual(substitute_token(("name", "x"), {"x": 4}), ("number", 4))

    def test_unknown_name(self):
        token = ("name", "y")
        self.assertEqual(substitute_token(token, {"x": 4}), token)

    def test_number(self):
        token = ("number", 2)
        self.assertEqual(substitute_token(token, {"x": 4}), token)

    def test_operator(self):
        token = ("operator", "+")
        self.assertEqual(substitute_token(token, {"x": 4}), token)

    def test_reserved_name_not_in_memory(self):
        token = ("name", "pi")
        self.assertEqual(substitute_token(token, {}), token)


class TestSubstituteVariables(unittest.TestCase):
    def test_two_variables(self):
        tokens = tokenize_scientific("x + y")
        result = substitute_variables(tokens, {"x": 2, "y": 3})
        self.assertEqual(result, [("number", 2), ("operator", "+"), ("number", 3)])

    def test_function_name_preserved(self):
        tokens = tokenize_scientific("sin(x)")
        result = substitute_variables(tokens, {"x": 2})
        self.assertEqual(result, [("name", "sin"), ("left_paren", "("),
                                  ("number", 2), ("right_paren", ")")])

    def test_constant_preserved(self):
        tokens = tokenize_scientific("x * pi")
        result = substitute_variables(tokens, {"x": 2})
        self.assertEqual(result, [("number", 2), ("operator", "*"), ("name", "pi")])


class TestEvaluateTokens(unittest.TestCase):
    def test_single_number(self):
        self.assertEqual(evaluate_tokens([("number", 5)]), 5)

    def test_expression(self):
        self.assertEqual(evaluate_tokens(tokenize_scientific("2 + 2 * 2")), 6)

    def test_empty(self):
        with self.assertRaises(ValueError):
            evaluate_tokens([])

    def test_not_finished(self):
        with self.assertRaises(ValueError):
            evaluate_tokens(tokenize_scientific("2 2"))


class TestAssignVariable(unittest.TestCase):
    def test_store_and_return(self):
        memory = make_memory()
        self.assertEqual(assign_variable("x", "2 + 2", memory), 4)
        self.assertEqual(memory, {"x": 4})

    def test_chain(self):
        memory = make_memory()
        self.assertEqual(assign_variable("a", "b = 2", memory), 2)
        self.assertEqual(memory, {"a": 2, "b": 2})

    def test_overwrite(self):
        memory = {"x": 1}
        self.assertEqual(assign_variable("x", "5", memory), 5)
        self.assertEqual(memory["x"], 5)


class TestCalculateWithMemory(unittest.TestCase):
    def test_plain_expression(self):
        self.assertEqual(calculate_with_memory("2 + 2", make_memory()), 4)

    def test_assignment_returns_value(self):
        memory = make_memory()
        self.assertEqual(calculate_with_memory("x = 2 + 2", memory), 4)
        self.assertEqual(memory, {"x": 4})

    def test_use_variable(self):
        memory = make_memory()
        calculate_with_memory("x = 2 + 2", memory)
        self.assertEqual(calculate_with_memory("x * 3", memory), 12)

    def test_variable_alone(self):
        self.assertEqual(calculate_with_memory("x", {"x": 4}), 4)

    def test_chained_assignment(self):
        memory = make_memory()
        self.assertEqual(calculate_with_memory("a = b = 3", memory), 3)
        self.assertEqual(memory, {"a": 3, "b": 3})

    def test_negative_value(self):
        memory = make_memory()
        calculate_with_memory("x = -3", memory)
        self.assertEqual(calculate_with_memory("x * x", memory), 9)

    def test_scientific_number_value(self):
        memory = make_memory()
        self.assertEqual(calculate_with_memory("x = 2e3", memory), 2000.0)

    def test_real_power_with_variable(self):
        memory = make_memory()
        calculate_with_memory("x = 2", memory)
        self.assertAlmostEqual(calculate_with_memory("x ^ 0.5", memory), 1.4142135623730951, places=12)

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            calculate_with_memory("y + 1", make_memory())

    def test_reserved_assignment_function(self):
        with self.assertRaises(ValueError):
            calculate_with_memory("sin = 2", make_memory())

    def test_reserved_assignment_constant(self):
        with self.assertRaises(ValueError):
            calculate_with_memory("pi = 3", make_memory())

    def test_constant_still_works(self):
        self.assertAlmostEqual(calculate_with_memory("x * pi", {"x": 2}), 6.283185307179586, places=12)

    def test_function_of_variable(self):
        memory = make_memory()
        calculate_with_memory("x = pi / 2", memory)
        self.assertAlmostEqual(calculate_with_memory("sin(x)", memory), 1.0, places=12)

    def test_empty_right_side(self):
        with self.assertRaises(ValueError):
            calculate_with_memory("x =", make_memory())

    def test_bad_left_side(self):
        with self.assertRaises(ValueError):
            calculate_with_memory("2 = 2", make_memory())


class TestMakeSession(unittest.TestCase):
    def test_shape(self):
        session = make_session()
        self.assertEqual(session["memory"], {})
        self.assertEqual(session["stack"], [])
        self.assertEqual(session["log"], [])

    def test_independent(self):
        first = make_session()
        second = make_session()
        first["stack"].append(1)
        self.assertEqual(second["stack"], [])


class TestRememberAnswer(unittest.TestCase):
    def test_stores_ans(self):
        session = make_session()
        remember_answer(session, 4)
        self.assertEqual(session["memory"]["ans"], 4)

    def test_overwrites(self):
        session = make_session()
        remember_answer(session, 4)
        remember_answer(session, 5)
        self.assertEqual(session["memory"]["ans"], 5)


class TestPushResult(unittest.TestCase):
    def test_appends_in_order(self):
        session = make_session()
        push_result(session, 4)
        push_result(session, 8)
        self.assertEqual(session["stack"], [4, 8])


class TestLogOperation(unittest.TestCase):
    def test_appends_pairs_in_order(self):
        session = make_session()
        log_operation(session, "1 + 1", 2)
        log_operation(session, "2 + 2", 4)
        self.assertEqual(session["log"], [("1 + 1", 2), ("2 + 2", 4)])


class TestRememberResult(unittest.TestCase):
    def test_all_three(self):
        session = make_session()
        remember_result(session, "2 + 2", 4)
        self.assertEqual(get_answer(session), 4)
        self.assertEqual(get_results(session), [4])
        self.assertEqual(get_log(session), [("2 + 2", 4)])


class TestGetAnswer(unittest.TestCase):
    def test_none_initially(self):
        self.assertIsNone(get_answer(make_session()))

    def test_after_remembering(self):
        session = make_session()
        remember_answer(session, 7)
        self.assertEqual(get_answer(session), 7)


class TestGetResults(unittest.TestCase):
    def test_order(self):
        session = make_session()
        push_result(session, 2)
        push_result(session, 4)
        self.assertEqual(get_results(session), [2, 4])

    def test_copy_is_independent(self):
        session = make_session()
        push_result(session, 1)
        results = get_results(session)
        results.append(999)
        self.assertEqual(get_results(session), [1])


class TestGetLog(unittest.TestCase):
    def test_entries(self):
        session = make_session()
        log_operation(session, "1 + 1", 2)
        self.assertEqual(get_log(session), [("1 + 1", 2)])

    def test_copy_is_independent(self):
        session = make_session()
        log_operation(session, "1 + 1", 2)
        log = get_log(session)
        log.append(("x", 0))
        self.assertEqual(get_log(session), [("1 + 1", 2)])


class TestCalculateSession(unittest.TestCase):
    def test_expression(self):
        session = make_session()
        self.assertEqual(calculate_session("2 + 2", session), 4)

    def test_ans_variable(self):
        session = make_session()
        calculate_session("2 + 2", session)
        self.assertEqual(calculate_session("ans * 2", session), 8)

    def test_variables_still_work(self):
        session = make_session()
        calculate_session("x = 2", session)
        self.assertEqual(calculate_session("x * 3", session), 6)
        self.assertEqual(session["memory"]["x"], 2)

    def test_assignment_updates_ans(self):
        session = make_session()
        calculate_session("x = 3 * 3", session)
        self.assertEqual(get_answer(session), 9)

    def test_stack_grows(self):
        session = make_session()
        calculate_session("1 + 1", session)
        calculate_session("2 + 2", session)
        self.assertEqual(get_results(session), [2, 4])

    def test_log_entries(self):
        session = make_session()
        calculate_session("1 + 1", session)
        calculate_session("2 + 2", session)
        self.assertEqual(get_log(session), [("1 + 1", 2), ("2 + 2", 4)])

    def test_division_error_no_trace(self):
        session = make_session()
        with self.assertRaises(ZeroDivisionError):
            calculate_session("1 / 0", session)
        self.assertIsNone(get_answer(session))
        self.assertEqual(get_results(session), [])
        self.assertEqual(get_log(session), [])

    def test_unknown_name_error_no_trace(self):
        session = make_session()
        calculate_session("2 + 2", session)
        with self.assertRaises(ValueError):
            calculate_session("y + 1", session)
        self.assertEqual(get_results(session), [4])
        self.assertEqual(get_log(session), [("2 + 2", 4)])

    def test_ans_in_function_call(self):
        session = make_session()
        calculate_session("x = pi / 2", session)
        self.assertAlmostEqual(calculate_session("sin(ans)", session), 1.0, places=12)

    def test_ans_before_first_calculation(self):
        with self.assertRaises(ValueError):
            calculate_session("ans + 1", make_session())

    def test_user_can_assign_ans(self):
        session = make_session()
        self.assertEqual(calculate_session("ans = 5", session), 5)
        self.assertEqual(get_answer(session), 5)


if __name__ == "__main__":
    unittest.main()