def get_amount_in_float(amt: str) -> float:
    return float(amt.split('$')[-1])
