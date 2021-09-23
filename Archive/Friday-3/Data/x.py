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


with open(r"F:\Python\Friday\Imperatives.csv", "r") as f:
    lines = [l for l in f]

data = []
for line in lines:
    enc = Brain().encoder(line)
    if enc in data:
        print(line)
        print(">>>", lines.index(line))
    else:
        data.append(enc)
        with open("NewImperatives2.csv", "a") as f:
            l = "\n" + line.strip()
            f.write(l)