import json, io, nltk

with open(r"F:\Python\Friday\Cache\Rudra.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for comment in data["data"]:
    category = data["data"][comment]

    value_set = {"statement": 0, "command": 1, "question": 2}


def create_word_embedding(comments, add_pos_tags=False):
    count = 0
    word_embedding = {}
    encoded_comments = []

    for comment in comments:
        comment = nltk.word_tokenize(comment.lower())
        if add_pos_tags:
            comment = [
                ele for word_tuple in nltk.pos_tag(comment) for ele in word_tuple
            ]

        # Creating mapping: { "this": 1, "is": 2, ... } & encode each comment
        encoded_comment = []
        for word in comment:
            if word not in word_embedding:
                word_embedding[word] = count
                count += 1
            encoded_comment.append(word_embedding[word])
        encoded_comments.append(encoded_comment)

    return encoded_comments


print(create_word_embedding(["Hi, what the heck are you up to?"]))