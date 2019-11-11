
def combinations(values, combos, current_combination, K, level=0, ind_previous_index=-1):
    if level >= K:
        combos.append(list(current_combination))
        return combos

    for i, v in enumerate(values):
        if i <= ind_previous_index:
            continue
        current_combination.append(v)
        combinations(values, combos, current_combination, K, level + 1, i)
        current_combination.pop()

    return combos


def filter_itemset(itemset, minsup):
    return dict(filter(lambda x: x[1] > minsup, itemset.items()))


def get_frequency(combo, transactions):
    c = 0
    for t in transactions:
        found = True
        for item in combo:
            if item not in t:
                found = False
                break
        if found:
            c += 1
    return c


def get_freq_itemset(transactions, combos, minsup):
    freq_item_set = {tuple(c): get_frequency(c, transactions) for c in combos}
    return filter_itemset(freq_item_set, minsup)


def apriori(transactions, minsup):
    freq_itemset = {}

    for t in transactions:
        for item in t:
            freq_itemset[item] = freq_itemset.get(item, 0) + 1

    # Frequent Itemset of lenght 1
    freq_itemset = filter_itemset(freq_itemset, minsup)
    distinct_values = list(freq_itemset.keys())
    K = len(freq_itemset)

    for i in range(2, K+1):
        combos = combinations(distinct_values, [], [], i)
        freq_itemset.update(get_freq_itemset(transactions, combos, minsup))

    return freq_itemset


if __name__ == '__main__':
    dataset = [['a', 'b'],
               ['b', 'c', 'd'],
               ['a', 'c', 'd', 'e'],
               ['a', 'd', 'e'],
               ['a', 'b', 'c'],
               ['a', 'b', 'c', 'd'],
               ['b', 'c'],
               ['a', 'b', 'c'],
               ['a', 'b', 'd'],
               ['b', 'c', 'e']]

    for k, v in apriori(dataset, 1).items():
        print(f"{k}: {v}")