import FPgrowth as fp
if __name__ == '__main__':

    transactions = [
        ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
        ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
        ['b', 'f', 'h', 'j', 'o'],
        ['b', 'c', 'k', 's', 'p'],
        ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
    ]

    grouped = fp.preprocess_transactions(transactions, min_sup=2)
    fp.fpgrowth(grouped,2)
