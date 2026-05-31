# tools/calculator_tool.py
import math
from langchain.tools import tool

@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Input: plain math expression e.g. 45 * 14
    Output: numerical result
    """
    try:
        expression = expression.strip().strip("\'\"")
        allowed = {k: getattr(math, k) for k in dir(math)
                   if not k.startswith("_")}
        allowed["__builtins__"] = {}
        result = eval(expression, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"
