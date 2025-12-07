"""Utilities for loading transactions from one-hot encoded CSV files.

The CSV is expected to have a header row with column names that
represent product/item identifiers. Each subsequent row represents a
transaction and contains truthy/falsy values indicating whether the
product was present in that transaction.

Example usage:
    from TransactionDB import TransactionDB
    transactions = TransactionDB.from_one_hot_csv('data.csv')

`transactions` will be a list of lists of item names suitable for
passing to `preprocess_transactions`.
"""

from typing import List, Iterable, Optional
import csv


class TransactionDB:
    @staticmethod
    def from_one_hot_csv(
        path: str,
        delimiter: str = ",",
        true_values: Optional[Iterable[str]] = None,
        drop_empty: bool = True,
    ) -> List[List[str]]:
        """Read a one-hot encoded CSV and return transactions.

        Parameters
        - path: path to the CSV file
        - delimiter: CSV delimiter (default: ',')
        - true_values: iterable of strings (case-insensitive) treated as
          truthy (e.g. {'1','yes','true'}). If None, a sensible default
          is used.
        - drop_empty: if True, rows that contain no truthy values are
          skipped.

        Returns a list of transactions, where each transaction is a
        list of column products names.
        """

        if true_values is None:
            true_values = {"1", "true", "t", "yes", "y"}
        true_set = {s.lower() for s in true_values}

        transactions: List[List[str]] = []

        with open(path, newline="") as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            try:
                header = next(reader)
            except StopIteration:
                return []

            for row in reader:
                if len(row) < len(header):
                    row += [""] * (len(header) - len(row))
                txn: List[str] = []
                for col_name, raw in zip(header, row):
                    s = raw.strip()
                    if not s:
                        continue
                    low = s.lower()
                    if low in true_set:
                        txn.append(col_name)
                        continue
                    try:
                        if float(s) != 0:
                            txn.append(col_name)
                    except Exception:
                        continue

                if txn or not drop_empty:
                    transactions.append(txn)

        return transactions


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: TransactionDB.py path/to/file.csv")
        raise SystemExit(1)

    path = sys.argv[1]
    txns = TransactionDB.from_one_hot_csv(path)
    print(f"Loaded {len(txns)} transactions")
    for t in txns[:10]:
        print(t)
