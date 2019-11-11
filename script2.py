import json
from apriori import apriori


def get_json(path):
    with open(path, encoding="utf8") as fp:
        return json.load(fp)


if __name__ == '__main__':
    dataset = get_json("data_sets/coco.json")

    # 2.
    transactions = list(map(lambda t: t['annotations'], dataset))
    #print(transactions[:10])

    print(apriori(transactions, 0.02))