"""
tools/calculator.py — Math, unit conversion, date/time utilities
No external API needed — pure Python.
"""
import math
import re
from datetime import datetime, timedelta
from langchain_core.tools import tool
from logger import get_logger

log = get_logger("tool.calc")


@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Supports: +, -, *, /, **, sqrt, sin, cos, tan, log, pi, e.
    Examples: '2**10', 'sqrt(144)', 'sin(pi/2)', '15% of 4500'.
    """
    log.info(f"Calculate: {expression}")
    try:
        expr = expression.lower().strip()

        # Percentage: "X% of Y"
        pct = re.match(r"(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)", expr)
        if pct:
            a, b = float(pct.group(1)), float(pct.group(2))
            result = (a / 100) * b
            return f"{a}% of {b} = {result:,.2f}"

        # Safe eval
        safe = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        safe.update({"abs": abs, "round": round, "min": min, "max": max})
        result = eval(expr, {"__builtins__": {}}, safe)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Could not calculate '{expression}': {e}"


@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert between common units.
    Supports: km/miles, kg/pounds, celsius/fahrenheit, meters/feet, liters/gallons.
    """
    log.info(f"Convert: {value} {from_unit} → {to_unit}")
    f, t = from_unit.lower().strip(), to_unit.lower().strip()
    v = value

    conversions = {
        ("km", "miles"):       v * 0.621371,
        ("miles", "km"):       v * 1.60934,
        ("kg", "pounds"):      v * 2.20462,
        ("pounds", "kg"):      v / 2.20462,
        ("kg", "lbs"):         v * 2.20462,
        ("lbs", "kg"):         v / 2.20462,
        ("meters", "feet"):    v * 3.28084,
        ("feet", "meters"):    v / 3.28084,
        ("liters", "gallons"): v * 0.264172,
        ("gallons", "liters"): v / 0.264172,
        ("celsius", "fahrenheit"): v * 9/5 + 32,
        ("fahrenheit", "celsius"): (v - 32) * 5/9,
        ("celsius", "kelvin"): v + 273.15,
        ("kelvin", "celsius"): v - 273.15,
        ("km", "m"):   v * 1000,
        ("m", "km"):   v / 1000,
        ("gb", "mb"):  v * 1024,
        ("mb", "gb"):  v / 1024,
        ("tb", "gb"):  v * 1024,
        ("gb", "tb"):  v / 1024,
    }

    result = conversions.get((f, t))
    if result is not None:
        return f"{value} {from_unit} = {result:.4f} {to_unit}"
    return f"Conversion {from_unit} → {to_unit} not supported yet."


@tool
def get_datetime_info(query: str = "now") -> str:
    """
    Get current date, time, day, or calculate date differences.
    Examples: 'now', 'tomorrow', 'days until 2025-12-31', 'what day is 2025-08-15'.
    """
    log.info(f"Datetime query: {query}")
    q = query.lower().strip()
    now = datetime.now()

    if q in ("now", "time", "current time"):
        return f"Current time: {now.strftime('%I:%M %p')} on {now.strftime('%A, %d %B %Y')}"

    if q in ("today", "date", "today's date"):
        return f"Today is {now.strftime('%A, %d %B %Y')}"

    if q == "tomorrow":
        tom = now + timedelta(days=1)
        return f"Tomorrow is {tom.strftime('%A, %d %B %Y')}"

    if q == "yesterday":
        yes = now - timedelta(days=1)
        return f"Yesterday was {yes.strftime('%A, %d %B %Y')}"

    # "days until YYYY-MM-DD"
    m = re.search(r"(\d{4}-\d{2}-\d{2})", q)
    if m:
        try:
            target = datetime.strptime(m.group(1), "%Y-%m-%d")
            diff   = (target - now).days
            if diff > 0:
                return f"{diff} days until {target.strftime('%d %B %Y')}"
            elif diff < 0:
                return f"{abs(diff)} days since {target.strftime('%d %B %Y')}"
            else:
                return "That's today!"
        except Exception:
            pass

    return f"Current: {now.strftime('%A, %d %B %Y — %I:%M %p')}"