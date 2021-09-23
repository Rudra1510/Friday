import json, nltk


class Encode:
    def __init__(self, statement):
        tokens = nltk.RegexpTokenizer(r"\w+").tokenize(statement.lower())
        tags = [tag for word, tag in nltk.pos_tag(tokens)]

        with open(r"Friday.json", "r") as f:
            data = json.loads(f.read())

        self.encoded = [data["tags"][tag] for tag in tags]

    def Raw(self):
        raw = [self.encoded.index(i) if i in self.encoded else 0 for i in range(0, 44)]
        return raw

    def Linear(self):
        for i in range(51 - len(self.encoded)):
            self.encoded.append(0)
        if len(self.encoded) > 51:
            self.encoded = self.encoded[:51]
        return self.encoded


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

        x_train = [Encode(comment).Linear() for comment in trainjson]
        y_train = [trainjson[comment] for comment in trainjson]
        x_test = [Encode(comment).Linear() for comment in testjson]
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

    Data().Create()

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.linear_model import LogisticRegression,LinearRegression
    from sklearn.metrics import accuracy_score

    [x_train, y_train, x_test, y_test] = Data().Get()

    tree = DecisionTreeClassifier().fit(x_train, y_train).predict(x_test)
    linear = LinearRegression().fit(x_train, y_train).predict(x_test)
    logic = LogisticRegression(max_iter=99999).fit(x_train, y_train).predict(x_test)
    
    print(accuracy_score(y_test, tree))
    # print(accuracy_score(y_test, linear))
    print(accuracy_score(y_test, logic))
