import stage_1
import stage_2


def main():
    income_earned = stage_2.main()
    staff_expenses = float(input("Staff expenses:\n"))
    other_expenses = float(input("Other expenses:\n"))
    net_income = income_earned - (staff_expenses + other_expenses)
    print(f"Net income: {net_income}")


if __name__ == "__main__":
    main()
