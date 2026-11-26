import pytest
from agent import run, calculator


def test_calculator():
    assert calculator("12*(3+4)") == 84


def test_calculator_rejects_code():
    with pytest.raises(Exception):
        calculator("__import__('os').system('echo hi')")


def test_math_question():
    assert run("What is 12 * (3 + 4)?")[0] == "84"


def test_lookup_question():
    assert "web framework" in run("what is fastapi")[0]


def test_unknown():
    assert run("Tell me a joke")[0] == "I cannot answer that."


def test_tool_error_is_reported():
    assert run("1/0")[0].startswith("error:")
