n_transactions = 0

def generate_combinations(itemset):
    combinations = []
    for i in range(len(itemset)):
        for j in range(i+1, len(itemset)):
            if itemset[i][:-1] == itemset[j][:-1]:
                combinations.append(itemset[i][:-1] + tuple(sorted([itemset[i][-1], itemset[j][-1]])))
    return combinations

def apriori(transactions, minsup):
    global n_transactions
    n_transactions = len(transactions)
    single_item_freq = {}

    for t in transactions:
        for item in t:
            single_item_freq[item.strip()] = single_item_freq.get(item.strip(), 0) + 1

    freq_itemset = [{(k,): v for k, v in single_item_freq.items() if v / n_transactions > minsup}]

    while freq_itemset[-1] != {}:
        combinations = generate_combinations(list(freq_itemset[-1].keys()))

        tmp_freq = {}
        for t in transactions:
            t_set = set(t)
            for c in combinations:
                c_set = set(c)
                if c_set.issubset(t_set):
                    tmp_freq[c] = tmp_freq.get(c, 0) + 1

        freq_itemset.append({k: v for k, v in tmp_freq.items() if v / n_transactions > minsup})

    return freq_itemset[:-1]




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
    
    freq = apriori(dataset, 0.1)
    print(sum(list(map(lambda x: len(x), freq))))
    for itemset in freq:
        for k, v in itemset.items():
            print(f"{k}: {v}")