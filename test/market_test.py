import os
import sys
from TransactionDB import TransactionDB
import FPgrowth as fp


def main(csv_path: str, min_sup: int = 50):
    transactions = TransactionDB.from_one_hot_csv(csv_path, delimiter=';')
    print(f"Loaded {len(transactions)} transactions from: {csv_path}")
    if len(transactions) == 0:
        print("No transactions found — exiting.")
        return

    grouped = fp.preprocess_transactions(transactions, min_sup=min_sup)
    print("Grouped transactions prepared. Running FP-growth:\n")
    fp.fpgrowth(grouped, min_sup)


if __name__ == '__main__':
    #create an absolute path to the csv file avoid any problem
    here = os.path.dirname(__file__)
    csv_path = os.path.normpath(os.path.join(here, '..', 'assets', 'market.csv'))
    min_sup = 3
    print(f"Running market test using: {csv_path} (min_sup={min_sup})\n")
    main(csv_path, min_sup)
