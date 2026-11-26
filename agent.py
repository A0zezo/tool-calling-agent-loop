"""A minimal tool-calling agent loop. The 'model' is a deterministic rule-based planner standing in for an LLM,
so the loop (plan -> call tool -> observe -> answer) runs offline and is testable. Swap `plan` for an LLM call to use a real model."""
import ast
import operator
import re

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}
FACTS = {"python": "Python is a programming language created by Guido van Rossum.", "fastapi": "FastAPI is a Python web framework for building APIs."}


def calculator(expr):
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("unsupported expression")
    return ev(ast.parse(expr, mode="eval").body)


def lookup(term):
    return FACTS.get(term.lower(), "no entry")


TOOLS = {"calculator": calculator, "lookup": lookup}


def plan(question, history):
    """Return ('call', tool, arg) or ('final', text)."""
    if history:
        return ("final", f"{history[-1][2]}")
    m = re.search(r"[\d(][\d\s+\-*/().^]*[\d)]", question)
    if m and any(c in question for c in "+-*/"):
        return ("call", "calculator", m.group().replace("^", "**"))
    m = re.search(r"what is (\w+)", question.lower())
    if m:
        return ("call", "lookup", m.group(1))
    return ("final", "I cannot answer that.")


def run(question, max_steps=3):
    history = []
    for _ in range(max_steps):
        step = plan(question, history)
        if step[0] == "final":
            return step[1], history
        _, tool, arg = step
        try:
            result = str(TOOLS[tool](arg))
        except Exception as e:
            result = f"error: {e}"
        history.append((tool, arg, result))
    return "step limit reached", history
