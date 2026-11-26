# tool-calling-agent-loop

A minimal tool-calling agent loop (plan, call tool, observe, answer) with a safe AST-based calculator and a lookup tool. The planner is a deterministic rule-based stand-in for an LLM so the loop runs offline and can be tested.

## Run

```bash
pip install -r requirements.txt
python demo.py
pytest
```

## Output (reproduced)

```
$ python3 demo.py
Q: What is 12 * (3 + 4)?
  trace: [('calculator', '12 * (3 + 4)', '84')]
  A: 84
Q: what is FastAPI
  trace: [('lookup', 'fastapi', 'FastAPI is a Python web framework for building APIs.')]
  A: FastAPI is a Python web framework for building APIs.
Q: Tell me a joke
  trace: []
  A: I cannot answer that.
Q: compute 1/0 please 1/0
  trace: [('calculator', '1/0', 'error: division by zero')]
  A: error: division by zero

$ pytest -q
6 passed in 0.01s
```

## Limits

- There is no LLM here. The planner uses regular expressions, so it only handles simple arithmetic and `what is X` questions. Replace `plan` with a model call to use the loop with a real LLM. The last demo question is deliberately odd and shows the error path.
