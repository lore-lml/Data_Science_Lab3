import json
import my_apriori as my_apr
import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth
import numpy as np
import timeit as tm


def get_json(path):
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


def get_possible_annotations(transactions):
    annotations = {item.strip() for t in transactions for item in t}
    return {a: i for i, a in enumerate(sorted(annotations))}


def build_matrix(item_set, transactions):
    matrix = np.zeros((len(transactions), len(item_set)), dtype=np.int_)

    for i, t in enumerate(transactions):
        for a in t:
            annotation_index = item_set[a]
            matrix[i, annotation_index] = 1

    return matrix


def tuples2frozenset(itemset, annotations):
    fi_myap = set()
    for it in itemset:
        fi_myap.update({(v / 5000, frozenset({annotations.get(k_) for k_ in k})) for k, v in it.items()})
    return fi_myap

if __name__ == '__main__':
    # 2.
    images = get_json("data_sets/coco.json")

    transactions = [list(set(im['annotations'])) for im in images]
    #print(transactions[:10])

    # 3.
    freq = my_apr.apriori(transactions, 0.02)
    # print(sum(list(map(lambda x: len(x), freq))))
    print(freq)

    """itemset = {'baseball bat', 'baseball glove', 'bench', 'person'}
    with_itemset = [im['image_id'] for im in images if itemset.issubset(set(im['annotations']))]
    print(with_itemset[30])"""

    # 4.
    possible_annotations = get_possible_annotations(transactions)
    #print(len(possible_annotations))
    matrix = build_matrix(possible_annotations, transactions)
    # print(matrix[:10, :10])
    df = pd.DataFrame(data=matrix, columns=possible_annotations.keys())
    ap = apriori(df, min_support=0.02)
    fpg = fpgrowth(df, min_support=0.02)

    my_tuple = tuples2frozenset(freq, possible_annotations)
    ap_tuple = {tuple(t) for t in ap.values}
    fpg_tuple = {tuple(t) for t in fpg.values}

    # Tutti e 3 gli algoritmi hanno dato risultato equivalente
    print(f"fpg_tuple == ap_tuple: {fpg_tuple == ap_tuple}")
    print(f"my_tuple == ap_tuple: {my_tuple == ap_tuple}")

    print("fpgrowth", tm.timeit(lambda: fpgrowth(df, 0.02), number=1))
    print("apriori", tm.timeit(lambda: apriori(df, 0.02), number=1))
    print("my_apriori", tm.timeit(lambda: my_apr.apriori(transactions, 0.02), number=1))



