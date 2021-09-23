from sklearn.linear_model import LinearRegression
from sklearn import tree
import pymongo
import random
import json
import os

"""
    what is your name [0, 0, 1, 0, 0, 0, 1, 1, 0] [0]
    who is your boss [0, 0, 1, 0, 0, 0, 1, 1, 0] [0]
    what is the time [0, 0, 0, 0, 0, 0, 1, 1, 1] [0]
    who was akbar [0, 0, 0, 0, 0, 0, 1, 1, 0] [1]
    where is maldives [0, 0, 0, 0, 0, 0, 0, 1, 0] [1]
    what are magnets [0, 0, 0, 0, 0, 0, 1, 1, 0] [1]



    # features = [[0, 0, 1, 0, 0, 0, 1, 1, 0],
    #             [0, 0, 1, 0, 0, 0, 1, 1, 0],
    #             [0, 0, 0, 0, 0, 0, 1, 1, 1],
    #             [0, 0, 0, 0, 0, 0, 1, 1, 0],
    #             [0, 0, 0, 0, 0, 0, 0, 1, 0],
    #             [0, 0, 0, 0, 0, 0, 1, 1, 0]
    #             ]
    # labels = [[0], [0], [0], [1], [1], [1]]


    2 https://www.youtube.com/watch?v=8qwowmiXANQ
    3 https://www.youtube.com/watch?v=Da-iHgrmHYg
    4 https://www.youtube.com/watch?v=k1SzvvFtl4w"""


class Engine:
    def __init__(self):
        pass

    def Decode(self, string):
        with open(r"F:\Python\Friday\data.json", "r") as f:
            data = json.loads(f.read())["data"]

        every, result, features = [], [], [name for name in data]

        for feature in features:
            every.extend(data[feature])

        given_sentence = string.lower().split()
        for word in given_sentence:
            for feature in features:
                if word in data[feature]:
                    result.append(feature)
                    break
                else:
                    result.append("var")

        binary = []
        for f in features:
            if f in result:
                binary.append(1)
            else:
                binary.append(0)

        return binary

    def Decide(self, binary):
        features = Database().Get("feature")
        labels = Database().Get("label")
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(features, labels)
        return clf.predict([binary])


class Engine2:
    def __init__(self):

        """

        "what":{
            "my":{"name":"Rudra", "middlename":"Vishal","lastname":"Barot","birthday":"15 Oct, 2004"},
            "your":{}
        }

        func() = Decide whether it is a statement to be noted or to be searched

            Make a NLP Dataset
            Make Decoder
            Deciding ML Engine
        """
        pass

    def Decode(self, string):
        with open(r"dataset.json", "r") as file:
            file_data = json.loads(file.read())
            questions = file_data["questions"]
            verbs = file_data["grammar"]["helping_verbs"]
            articles = file_data["grammar"]["articles"]
            possessive = file_data["grammar"]["possessive"]

            list_s = [questions, verbs, articles, possessive]

        results = []
        index = []
        result = None
        given_sentence = string.lower().split()

        for word in given_sentence:

            for list_ in list_s:
                if word in list_:
                    results.append(1)
                    index.append(list_.index)

            # if word in questions:
            #     results.append(1)
            #     index.append(questions.index(word))
            #     continue

            # elif word in verbs:
            #     results.append(1)
            #     continue

            # elif word in possessive:
            #     results.append(1)
            #     continue

            # elif word in articles:
            #     results.append(1)
            #     continue

            # else:
            #     results.append(word)

        print(results)


class Database:
    def __init__(self):
        self.URI = "mongodb+srv://dbUser:dbUserPassword@cluster0.2akd2.mongodb.net/FridayServer?retryWrites=true&w=majority"
        self.database = "NLPDB"
        self.collection = "FLDB"

        self.client = pymongo.MongoClient(self.URI)
        self.db = self.client[self.database]
        self.col = self.db[self.collection]

    def Create(self, i):
        path = f"F:\Python\Friday\dataset{i}.txt"
        with open(path, "r") as file:
            lines = [line.strip() for line in file]
        binaries, result = [Engine().Decode(line) for line in lines], []
        [result.append(x) for x in binaries if x not in result]
        [self.col.insert_one({"feature": binary, "label": i}) for binary in result]

    def Get(self, key):
        cursor = self.col.find()
        values = [x[key] for x in cursor]
        return values

    def Clear(self):
        self.col.drop()


Engine2().Decode("what is your name")

# print(Database().Clear())

# while True:
#     binary = Engine().Decode(input('Input : '))
#     print(binary)
#     print(Engine().Decide(binary))

# Engine().ClearDatabase()
# Engine().CreateDatabase(0)
# Engine().CreateDatabase(1)

# for x in Engine().GetDatabase('feature'): print(x)
# for x in Engine().GetDatabase('label'): print(x)

# print(Engine().GetDatabase('feature'))
# print(Engine().GetDatabase('feature')[0])