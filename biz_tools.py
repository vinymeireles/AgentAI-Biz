# biz_tools.py
def safe_float(x):
    try:
        return float(x)
    except Exception:
        return 0.0

def format_currency(value, symbol="R$"):
    try:
        return f"{symbol} {float(value):,.2f}"
    except Exception:
        return f"{symbol} 0.00"
