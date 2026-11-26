from agent import run

for q in ["What is 12 * (3 + 4)?", "what is FastAPI", "Tell me a joke", "compute 1/0 please 1/0"]:
    ans, hist = run(q)
    print(f"Q: {q}\n  trace: {hist}\n  A: {ans}")
