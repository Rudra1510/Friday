import nltk
import json
import numpy as np
from sklearn import preprocessing


class Func:
    def encode(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokens)
        tags = [tag for word, tag in tags]

        with open(r"F:\Python\Friday\Try 3\friday.json", "r") as f:
            data = json.loads(f.read())

        encoded = [data["tags"][tag] for tag in tags]

        enc = [encoded.index(i) if i in encoded else 0 for i in range(0, 44)]
        return enc

    def nonquery(self, sentence):

        with open(r"F:\Python\Friday\dataset0.txt", "r") as f_1:
            lines_1 = [line_1 for line_1 in f_1]
            features_1 = []
            [
                features_1.append(Func().encode(l))
                for l in lines_1
                if Func().encode(l) not in lines_1
            ]
            labels_1 = [1 for i in range(len(features_1))]

        with open(r"F:\Python\Friday\dataset1.txt", "r") as f_0:
            lines_0 = [line_0 for line_0 in f_0]
            features_0 = []
            [
                features_0.append(Func().encode(l))
                for l in lines_0
                if Func().encode(l) not in lines_0
            ]
            labels_0 = [0 for i in range(len(features_0))]

        features = features_0 + features_1
        labels = labels_0 + labels_1

        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeClassifier

        model1 = LinearRegression().fit(features, labels)
        model2 = DecisionTreeClassifier().fit(features, labels)

        test = [Func().encode(sentence.lower())]
        return [model1.predict(test), model2.predict(test)]

    def query(self, sentence):

        with open(r"F:\Python\Friday\dataset1.txt", "r") as f_1:
            lines_1 = [line_1 for line_1 in f_1]
            features_1 = []
            [
                features_1.append(Func().encode(l))
                for l in lines_1
                if Func().encode(l) not in lines_1
            ]
            labels_1 = [1 for i in range(len(features_1))]

        with open(r"F:\Python\Friday\dataset0.txt", "r") as f_0:
            lines_0 = [line_0 for line_0 in f_0]
            features_0 = []
            [
                features_0.append(Func().encode(l))
                for l in lines_0
                if Func().encode(l) not in lines_0
            ]
            labels_0 = [0 for i in range(len(features_0))]

        features = features_0 + features_1
        labels = labels_0 + labels_1

        from sklearn.linear_model import LinearRegression
        from sklearn.tree import DecisionTreeClassifier

        model1 = LinearRegression().fit(features, labels)
        model2 = DecisionTreeClassifier().fit(features, labels)

        test = [Func().encode(sentence.lower())]
        return [model1.predict(test), model2.predict(test)]

    def linear(self, sentence):
        test = [Func().encode(sentence.lower())]
        features, labels = [], []

        with open(r"F:\Python\Friday\Try 3\friday.json", "r") as f:
            data = json.loads(f.read())

        keys = [_ for _ in data["sentences"]]
        for key in keys:
            label = keys.index(key)
            for sent in data["sentences"][key]:
                e = Func().encode(sent)
                if e in features:
                    print(sent)
                    print(e)
                    print(features.index(e))
                else:
                    features.append(e)
                    labels.append(label)

        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.tree import DecisionTreeClassifier

        clf = DecisionTreeClassifier().fit(features, labels)
        model = LinearRegression().fit(features, labels)
        logic = LogisticRegression().fit(features, labels)

        return [clf.predict(test), model.predict(test), logic.predict(test)]


if __name__ == "__main__":
    while True:
        take = input("Input:")
        give = Func().linear(take)

        answer1 = ((give[0] + give[1] + give[2]) / 3)[0]
        ans2 = round(answer1)

        print(give, answer1, ans2)
