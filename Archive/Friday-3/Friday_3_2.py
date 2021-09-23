import nltk, json


class Brain:
    def encoder(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokens)
        tags = [tag for word, tag in tags]

        with open(r"Friday.json", "r") as f:
            data = json.loads(f.read())

        encoded = [data["tags"][tag] for tag in tags]

        enc = [encoded.index(i) if i in encoded else 0 for i in range(0, 44)]
        return enc

    def linear(self, sentence):
        test = [Brain().encoder(sentence.lower())]

        features, labels = [], []

        with open(r"Friday.json", "r") as f:
            data = json.loads(f.read())

        keys = [stype for stype in data["sentences"]]
        for key in keys:
            label = keys.index(key)
            for sent in data["sentences"][key]:
                features.append(Brain().encoder(sent))
                labels.append(label)

        # Imperatives CSV
        # with open("Imperatives.csv", "r") as f:
        #     ilines = [line.strip() for line in f]
        # for iline in ilines:
        #     features.append(Brain().encoder(iline))
        #     labels.append(3)

        from sklearn.linear_model import LinearRegression, LogisticRegression
        from sklearn.tree import DecisionTreeClassifier

        tree = DecisionTreeClassifier().fit(features, labels)
        linear = LinearRegression().fit(features, labels)
        logic = LogisticRegression(max_iter=999999).fit(features, labels)

        return [tree.predict(test), linear.predict(test), logic.predict(test)]


if __name__ == "__main__":
    while True:
        take = input("Input:")
        r = Brain().linear(take)
        avg = ((r[0] + r[1] + r[2]) / 3)[0]
        Final = round(avg)

        print(r, avg, Final)

#     Brain().linear("Hi")
#     # Brain().test()

# # with open("Imperatives.csv", "r") as f:
# #     # print(f)
# #     # print(f.read())
# #     for line in f:
# #         print(line.strip())
