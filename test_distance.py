import random
import string
from timeit import timeit
from difflib import SequenceMatcher

from Levenshtein import distance
import pytest
import nim_str_utils

random.seed(42)


def find_common_substring_py(s1, s2, to_lower=True):
    if to_lower:
        s1 = s1.lower()
        s2 = s2.lower()
    m = SequenceMatcher(None, s1, s2, autojunk=False)
    match = m.find_longest_match(0, len(s1), 0, len(s2))
    return s1[match.a : match.a + match.size]


def find_common_sequence_py(s1, s2, to_lower=True):
    # mostly stolen from rosettacode.org
    if to_lower:
        a = s1.lower()
        b = s2.lower()
    else:
        a, b = s1, s2
    lengths = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])

    result = ""
    j = len(b)
    for i in range(1, len(a) + 1):
        if lengths[i][j] != lengths[i - 1][j]:
            result += a[i - 1]

    return result


def levenstein_py(s1, s2, to_lower=True):
    if to_lower:
        s1 = s1.lower()
        s2 = s2.lower()
    return distance(s1, s2)


def random_string(length):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def contains_one_of_py(s, seq, to_lower=True):
    s = s.lower() if to_lower else s
    return any(x in s for x in seq)


def contains_constant(seq, to_lower=True):
    return any("constant" in x for x in seq)


substrings = [random_string(10) for _ in range(100)]
line_a, line_b = (
    "BOLT.EU/O/2112171922. Merchant name: BOLT.EU/O/2112171922",
    "BOLT.EU/O/2201301820. Merchant name: BOLT.EU/O/2201301820",
)


@pytest.mark.parametrize("to_lower", [True, False])
def test_find_common_substring(to_lower):
    assert nim_str_utils.contains_one_of(
        line_a, substrings, to_lower
    ) == contains_one_of_py(line_a, substrings, to_lower)
    assert nim_str_utils.contains_constant(
        substrings, to_lower
    ) == contains_constant(substrings, to_lower)
    assert nim_str_utils.find_common_substring(
        line_a, line_b, to_lower
    ) == find_common_substring_py(line_a, line_b, to_lower)
    assert nim_str_utils.find_common_sequence(
        line_a, line_b, to_lower
    ) == find_common_sequence_py(line_a, line_b, to_lower)
    assert nim_str_utils.levenshtein_distance(
        line_a, line_b, to_lower
    ) == levenstein_py(line_a, line_b, to_lower)


def test_benchmark():
    n_runs = 10000
    print("\tContains one of")
    print(
        f"Python: {timeit(lambda: contains_one_of_py(line_a, substrings), number=n_runs):.3f}"
    )
    print(
        f"Nim: {timeit(lambda: nim_str_utils.contains_one_of(line_a, substrings), number=n_runs):.3f}"
    )

    print("\tContains constant")
    print(
        f"Python: {timeit(lambda: contains_constant(substrings), number=n_runs):.3f}"
    )
    print(
        f"Nim: {timeit(lambda: nim_str_utils.contains_constant(substrings), number=n_runs):.3f}"
    )
    print("\tFinding common string")
    print(
        f"Python: {timeit(lambda: find_common_substring_py(line_a, line_b), number=n_runs):.3f}"
    )
    print(
        f"Nim: {timeit(lambda: nim_str_utils.find_common_substring(line_a, line_b), number=n_runs):.3f}"
    )

    print("\tFinding common sequence")
    print(
        f"Python: {timeit(lambda: find_common_sequence_py(line_a, line_b), number=n_runs):.3f}"
    )
    print(
        f"Nim: {timeit(lambda: nim_str_utils.find_common_sequence(line_a, line_b), number=n_runs):.3f}"
    )

    print("\tLevenshtein distance")
    print(f"Python: {timeit(lambda: levenstein_py(line_a, line_b), number=n_runs):.3f}")
    print(
        f"Nim: {timeit(lambda: nim_str_utils.levenshtein_distance(line_a, line_b), number=n_runs):.3f}"
    )
