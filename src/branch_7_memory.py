# Ветвь 7. Память и история: переменные, ans, стек результатов
# и журнал операций.
# Часть 1 — переменные: присваивание "x = 2 + 2" и использование
# переменных в научных выражениях "x * 3". Часть 2 — сессия:
# ans (последний результат, доступен как обычная переменная),
# стек результатов и журнал операций. Память и сессию создаёт
# владелец (тест или интерфейс) и передаёт методам параметром;
# глобального состояния нет (docs/conventions.txt, раздел 6).
# Собирается из методов Ветвей 3a, 6a и 6b; существующие ветви
# не изменяются.

from branch_3a_tokenizer import make_token
from branch_6a_scientific_tokenizer import tokenize_scientific, is_letter
from branch_6b_scientific_parser import (
    parse_expression_scientific, is_function, is_constant,
)


def make_memory():
    """Создаёт пустую память калькулятора — словарь переменных."""
    return {}


def find_equals(s):
    """Возвращает позицию первого символа '=' в строке s или -1, если его нет."""
    return s.find("=")


def is_valid_name(s):
    """Возвращает True, если строка s — непустое имя из латинских букв."""
    if s == "":
        return False
    for c in s:
        if not is_letter(c):
            return False
    return True


def split_assignment(s):
    """Разбирает присваивание: возвращает пару (имя, выражение) без крайних пробелов или None, если '=' нет."""
    pos = find_equals(s)
    if pos == -1:
        return None
    name = s[:pos].strip()
    if not is_valid_name(name):
        raise ValueError("Слева от '=' может стоять только имя переменной (латинские буквы).")
    return name, s[pos + 1:].strip()


def is_reserved_name(name):
    """Возвращает True, если имя name занято константой или функцией: pi, e, sqrt, sin, ..."""
    return is_function(name) or is_constant(name)


def substitute_token(token, memory):
    """Заменяет токен-имя переменной на токен-число с её значением; прочие токены не меняет."""
    kind, value = token
    if kind == "name" and value in memory:
        return make_token("number", memory[value])
    return token


def substitute_variables(tokens, memory):
    """Заменяет в списке токенов имена переменных на их значения из памяти."""
    result = []
    for token in tokens:
        result.append(substitute_token(token, memory))
    return result


def evaluate_tokens(tokens):
    """Вычисляет значение полного списка научных токенов (с проверкой конца)."""
    if not tokens:
        raise ValueError("Пустое выражение.")
    value, pos = parse_expression_scientific(tokens, 0)
    if pos != len(tokens):
        raise ValueError("Выражение разобрано не до конца.")
    return value


def assign_variable(name, rhs, memory):
    """Вычисляет выражение rhs, сохраняет результат в память под именем name и возвращает его."""
    value = calculate_with_memory(rhs, memory)
    memory[name] = value
    return value


def calculate_with_memory(s, memory):
    """Вычисляет выражение или присваивание с переменными; память memory изменяется."""
    assignment = split_assignment(s)
    if assignment is not None:
        name, rhs = assignment
        if is_reserved_name(name):
            raise ValueError("Имя '" + name + "' занято константой или функцией.")
        return assign_variable(name, rhs, memory)
    return evaluate_tokens(substitute_variables(tokenize_scientific(s), memory))


# --- Часть 2. Сессия: ans, стек результатов и журнал операций ---


def make_session():
    """Создаёт пустую сессию калькулятора: память, стек результатов и журнал операций."""
    return {"memory": make_memory(), "stack": [], "log": []}


def remember_answer(session, value):
    """Сохраняет value как последний результат — переменную ans в памяти сессии."""
    session["memory"]["ans"] = value


def push_result(session, value):
    """Добавляет value в конец стека результатов сессии."""
    session["stack"].append(value)


def log_operation(session, text, value):
    """Добавляет пару (text, value) в журнал операций сессии."""
    session["log"].append((text, value))


def remember_result(session, text, value):
    """Запоминает результат value строки text сразу в ans, стек и журнал."""
    remember_answer(session, value)
    push_result(session, value)
    log_operation(session, text, value)


def get_answer(session):
    """Возвращает последний результат ans или None, если вычислений ещё не было."""
    return session["memory"].get("ans")


def get_results(session):
    """Возвращает копию стека результатов сессии: от первого вычисления к последнему."""
    return list(session["stack"])


def get_log(session):
    """Возвращает копию журнала операций: список пар (строка, результат)."""
    return list(session["log"])


def calculate_session(s, session):
    """Вычисляет выражение или присваивание в сессии; результат запоминается в ans, стек и журнал."""
    value = calculate_with_memory(s, session["memory"])
    remember_result(session, s, value)
    return value