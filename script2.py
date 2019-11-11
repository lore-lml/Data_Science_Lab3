import json


def get_json(path):
    with open(path, encoding="utf8") as fp:
        return json.load(fp)

if __name__ == '__main__':
    dataset = get_json("data_sets/coco.json")
    