with open(r"F:\Python\Friday\Data\FImperatives.csv", "r") as f:
    file = [l for l in f]

import nltk, json


class Brain:
    def encoder(self, sentence):
        tokens = nltk.RegexpTokenizer(r"\w+").tokenize(sentence)
        tags = nltk.pos_tag(tokens)
        tags = [tag for word, tag in tags]

        with open(r"Friday.json", "r") as f:
            data = json.loads(f.read())

        encoded = [data["tags"][tag] for tag in tags]

        enc = [encoded.index(i) if i in encoded else 0 for i in range(0, 44)]
        return enc


for line in file:
    enc = Brain().encoder(line)
    with open(r"Data\\Encoded\\EncImperative.csv", "a") as f:
        w = str(enc) + "\n"
        f.write(w)
