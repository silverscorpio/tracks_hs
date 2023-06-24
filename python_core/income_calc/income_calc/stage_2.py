from data import monthly_income
from utils import get_amount_in_float


def main() -> float:
    print("Earned amount:")
    for k, v in monthly_income.items():
        print(f"{k}: {v}")
    income = sum([float(get_amount_in_float(amt=v)) for v in monthly_income.values()])
    print(f"\nIncome: {income}")
    return income


if __name__ == "__main__":
    main()
