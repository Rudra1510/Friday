import json, nltk


def Encode(statement):
    with open(r"Friday.json", "r") as f:
        data = json.loads(f.read())
    tokens = nltk.RegexpTokenizer(r"\w+").tokenize(statement.lower())
    tags = [tag for word, tag in nltk.pos_tag(tokens)]

    encoded = [data["tags"][tag] for tag in tags]
    for i in range(51 - len(encoded)):
        encoded.append(0)
    if len(encoded) > 51:
        encoded = encoded[:51]

    return encoded


class Data:
    def __init__(self):
        pass

    def Get(self):
        with open(r"F:\Python\Friday\Cache.json", "r") as f:
            data = json.load(f)

        x_train = data["x_train"]
        y_train = data["y_train"]
        x_test = data["x_test"]
        y_test = data["y_test"]

        return [x_train, y_train, x_test, y_test]

    def Create(self):
        with open(r"Friday.json", "r") as f:
            rawdata = json.loads(f.read())

        trainjson = rawdata["Train"]
        testjson = rawdata["Test"]

        x_train = [Encode(comment) for comment in trainjson]
        y_train = [trainjson[comment] for comment in trainjson]
        x_test = [Encode(comment) for comment in testjson]
        y_test = [testjson[comment] for comment in testjson]

        FridayData = {
            "x_train": x_train,
            "y_train": y_train,
            "x_test": x_test,
            "y_test": y_test,
        }

        with open(r"Cache.json", "w") as f:
            json.dump(FridayData, f, indent=4)


if __name__ == "__main__":

    # Data().Create()

    from sklearn.tree import DecisionTreeClassifier

    [x_train, y_train, x_test, y_test] = Data().Get()
    tree = DecisionTreeClassifier().fit(x_train, y_train)

    while True:
        take = input("Input: ")

        if take == "q":
            quit()

        feature = Encode(take)
        print(tree.predict([feature]))

    # from sklearn.metrics import accuracy_score
    # print(accuracy_score(y_test, tree))
