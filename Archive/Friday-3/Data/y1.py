import nltk, json


def Encoder(sentence):
    tags = nltk.pos_tag(nltk.RegexpTokenizer(r"\w+").tokenize(sentence))
    pos_tags = [tag for word, tag in tags]
    with open(r"Friday.json", "r") as f:
        data = json.loads(f.read())
    tag_values = [data["tags"][tag] for tag in pos_tags]
    encoded = [tag_values.index(i) if i in tag_values else 0 for i in range(0, 44)]

    return encoded


# Encoder("Hi")
with open(r"F:\Python\Friday\Data\UnEncoded\UnEncImperatives.csv", "r") as f:
    lines = [l.strip() for l in f]

# e = [Encoder(l) for l in lines]

print(e)
