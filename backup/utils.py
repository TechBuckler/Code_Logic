def safe_eval(expr, context):
    try:
        return eval(expr, {}, context)
    except Exception:
        return False
