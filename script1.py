import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
import csv
import numpy as np

header = ""
n_cols = 0
INVOICE_N_I = 0
ITEM_DESC_I = 2
MINSUP = 0.02


def csv2list(path):
    with open(path, encoding="utf8") as fp:
        global header, n_cols
        reader = csv.reader(fp)
        header = list(next(reader))
        n_cols = len(header)
        dataset = [[] for i in range(n_cols)]
        c = 0
        for rows in reader:
            c += 1
            if len(rows) != n_cols or rows[0][0].lower() == "c":
                continue
            for i in range(n_cols):
                dataset[i].append(rows[i].strip())

        # print(c)
        return dataset


def get_transactions(dataset):
    transactions = {}

    for i in range(len(dataset[INVOICE_N_I])):
        try:
            (transactions[dataset[INVOICE_N_I][i]]).append(dataset[ITEM_DESC_I][i])
        except KeyError:
            transactions[dataset[INVOICE_N_I][i]] = [dataset[ITEM_DESC_I][i]]

    """for invoice in transactions.keys():
        transactions[invoice].sort()"""

    return transactions


def build_item_matrix(items, transactions):
    matrix = np.zeros((len(transactions), len(items)), dtype=np.int_)

    for i, t in enumerate(transactions.values()):
        for item in t:
            j = items[item]
            matrix[i, j] = 1

    return matrix


if __name__ == '__main__':
    # 1.
    dataset = csv2list("data_sets/online_retail.csv")
    # print(len(dataset[0]))

    # 2.
    transactions = get_transactions(dataset)
    # print(list(transactions.keys())[:5])
    # print(list(transactions.values())[:5])

    # 3.
    all_possible_items = {item for t in transactions.values() for item in t}
    all_possible_items = {item: index for index, item in enumerate(sorted(all_possible_items))}
    # print(all_possible_items)
    matrix = build_item_matrix(all_possible_items, transactions)
    # print(matrix[0, 3687])
    df = pd.DataFrame(data=matrix, columns=all_possible_items.keys())

    # 4.
    """for minsup in [0.5, 0.1, 0.05, 0.02, 0.01]:
        freq_itemsets = fpgrowth(df, minsup)
        print(f"{minsup} => {len(freq_itemsets)}")"""

    # Itemset that appears in 10% of transactions
    itemset_10 = fpgrowth(df, 0.1)
    print(itemset_10.to_string())
    print(list(all_possible_items.keys())[3893])
    print(f"{100* df.values[:, 3893].sum() / len(df)}")

    # 5.
    itemset_002 = fpgrowth(df, MINSUP)
    print(itemset_002[itemset_002["itemsets"].map(len) > 1])

    # 6.
    # (1587, 2644) -> 1587 => 2644 and 2644 => 1587
    mask_1587 = matrix[:, 1587] == 1
    support_1587 = len(matrix[mask_1587]) / len(matrix)
    mask_2644 = matrix[:, 2644] == 1
    support_2644 = len(matrix[mask_2644]) / len(matrix)
    mask_both = mask_1587 & mask_2644
    support_both = len(matrix[mask_both]) / len(matrix)
    print(f"Support 1587, 2644, both")
    print(f"{support_1587} {support_2644} {support_both}")

    print(f"Confidence 1587 => 2644: {support_both / support_1587}")
    print(f"Confidence 2644 => 1587: {support_both / support_2644}\n")

    # 7.
    itemset_001 = fpgrowth(df, 0.01)
    ass_rules = association_rules(itemset_001, "confidence", 0.85)
    print(ass_rules)
    print(ass_rules['confidence'])