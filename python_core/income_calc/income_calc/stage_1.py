""" Stage 1 """

from data import prices


def main():
    print("Prices:")
    for k, v in prices.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
