import os
import time
import json
import random
import datetime
import nltk
import numpy as np
import tensorflow as tf
from googlesearch import search
from sklearn.tree import DecisionTreeClassifier

# nltk = None
# np = None
# tf = None
# search = None
# DecisionTreeClassifier = None

#%%
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def Encode(Text, Binary):
    with open(r"/content/Friday.json", "r") as f:
        data = json.loads(f.read())

    tokens = nltk.RegexpTokenizer(r"\w+").tokenize(Text.lower().strip())
    tags = [tag for word, tag in nltk.pos_tag(tokens)]
    encoded = [data["tags"][tag] for tag in tags]

    if len(encoded) > 51:
        encoded = encoded[:51]
    else:
        for i in range(51 - len(encoded)):
            encoded.append(0)

    if Binary == False:
        return encoded
    elif Binary == True:
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=51)
        encoded = tokenizer.sequences_to_matrix([encoded], mode="binary")
        return encoded[0].tolist()

#%%
class Data:
    def __init__(self):
        pass
 
    #timeit
    def Create(self, BinaryFormat, Run):
        if Run == True:
            with open(r"/content/Friday.json", "r") as f:
                RawData = json.loads(f.read())
 
            TrainJson = RawData["Train"]
            TestJson = RawData["Test"]
 
            X = [Encode(comment, BinaryFormat) for comment in TrainJson]
            Y = [TrainJson[comment] for comment in TrainJson]
            x = [Encode(comment, BinaryFormat) for comment in TestJson]
            y = [TestJson[comment] for comment in TestJson]
 
            FridayData = {"X": X, "Y": Y, "x": x, "y": y}
 
            with open(r"/content/Encoded.json", "w") as f:
                json.dump(FridayData, f, indent=4)
        elif Run == False:
            pass
 
    #timeit
    def Get(self):
        with open(r"/content/Encoded.json", "r") as f:
            EncodedData = json.load(f)
 
        X = EncodedData["X"]
        Y = EncodedData["Y"]
        x = EncodedData["x"]
        y = EncodedData["y"]
 
        Classes = np.max(Y) + 1
 
        Y = tf.keras.utils.to_categorical(Y, Classes)
        y = tf.keras.utils.to_categorical(y, Classes)
 
        MaxWords = 51
        BatchSize = 256
        Epochs = 10
 
        return [X, Y, x, y, Classes, MaxWords, BatchSize, Epochs]
#%%
class Predict:
    def __init__(self, Text, Create=False):
        self.Text = Encode(Text, True)
        Data().Create(BinaryFormat=True, Run=Create)
        [
            self.X,
            self.Y,
            self.x,
            self.y,
            self.Classes,
            self.MaxWords,
            self.BatchSize,
            self.Epochs,
        ] = Data().Get()

    #timeit
    def Sklearn(self):

        self.Prediction = (
            DecisionTreeClassifier().fit(self.X, self.Y).predict([self.Text])
        )
        return np.argmax(self.Prediction)

class TF:
    def __init__(self, Create=False):
        Data().Create(BinaryFormat=True, Run=Create)
        [
            self.X,
            self.Y,
            self.x,
            self.y,
            self.Classes,
            self.MaxWords,
            self.BatchSize,
            self.Epochs,
        ] = Data().Get()
        self.model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Dense(
                    self.MaxWords, input_shape=(self.MaxWords,), activation="tanh"
                ),
                tf.keras.layers.Dense(2 * self.MaxWords, activation="tanh"),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(3, activation="softmax"),
            ]
        )
        self.model.compile(
            optimizer="adam", metrics=["accuracy"], loss="categorical_crossentropy"
        )
        self.model.fit(
            np.array(self.X),
            np.array(self.Y),
            batch_size=self.BatchSize,
            epochs=0,
            verbose=0,
        )

    def Show(self, Text):
        self.Text = Encode(Text, True)
        self.Prediction = self.model.predict([self.Text])
        return np.argmax(self.Prediction)

Predictor = TF(True)